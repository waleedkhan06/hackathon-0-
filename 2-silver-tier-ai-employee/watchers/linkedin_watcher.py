"""
LinkedIn Watcher for AI Employee Silver Tier
Monitors needs_action/ for LinkedIn post requests and creates approvals

Silver Tier Requirements:
- Monitor LinkedIn post requests
- Create approval files for HITL workflow
- Post to LinkedIn via browser automation (Playwright)
- Human-in-the-loop approval required before posting
"""
import time
import logging
from pathlib import Path
from datetime import datetime
import sys

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from watchers.base_watcher import BaseWatcher


class LinkedInWatcher(BaseWatcher):
    """
    LinkedIn Watcher - Monitors and creates approvals
    Posting handled by skills/linkedin_poster.py with Playwright
    """
    
    def __init__(self, project_path: str = None, check_interval: int = 30):
        if project_path is None:
            self.project_path = project_root
        else:
            self.project_path = Path(project_path)
        
        self.needs_action = self.project_path / 'needs_action'
        self.pending_approval = self.project_path / 'pending_approval'
        self.approved = self.project_path / 'approved'
        self.done = self.project_path / 'done'
        self.session_path = self.project_path / 'sessions' / 'linkedin'
        self.check_interval = check_interval
        self.processed_files = set()
        
        # Setup logging
        log_dir = self.project_path / 'logs'
        log_dir.mkdir(exist_ok=True)
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_dir / f'linkedin_watcher_{datetime.now().strftime("%Y%m%d")}.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(self.__class__.__name__)
        
        # Create directories
        self.needs_action.mkdir(exist_ok=True)
        self.pending_approval.mkdir(exist_ok=True)
        self.approved.mkdir(exist_ok=True)
        self.done.mkdir(exist_ok=True)
        self.session_path.mkdir(parents=True, exist_ok=True)
        
        self.logger.info("LinkedIn Watcher initialized")
    
    def check_for_updates(self) -> list:
        """Check for new LinkedIn post requests"""
        new_files = []
        
        for file_path in self.needs_action.glob('LINKEDIN_*.md'):
            if str(file_path) not in self.processed_files:
                content = file_path.read_text()
                if 'type: linkedin_post' in content.lower() or 'type: linkedin_post_request' in content.lower():
                    new_files.append(file_path)
                    self.processed_files.add(str(file_path))
                    self.logger.info(f"New LinkedIn post request: {file_path.name}")
        
        return new_files
    
    def check_approved_posts(self) -> list:
        """Check for approved posts ready to publish"""
        approved_files = []
        
        for file_path in self.approved.glob('LINKEDIN_*.md'):
            if str(file_path) not in self.processed_files:
                content = file_path.read_text()
                if 'action: linkedin_post' in content:
                    approved_files.append(file_path)
                    self.logger.info(f"Approved post ready: {file_path.name}")
        
        return approved_files
    
    def create_action_file(self, file_path: Path) -> Path:
        """Create approval request for LinkedIn post"""
        try:
            content = file_path.read_text()
            
            # Extract post content
            if '## Post Content' in content:
                post_content = content.split('## Post Content')[1].strip()
                post_content = post_content.replace('```', '').strip()
            elif '## Content' in content:
                post_content = content.split('## Content')[1].strip()
                post_content = post_content.replace('```', '').strip()
            else:
                post_content = content[:500]
            
            # Extract topic
            topic = 'Business Update'
            if 'topic:' in content:
                for line in content.split('\n'):
                    if 'topic:' in line:
                        topic = line.split('topic:')[1].strip()
                        break
            
            # Create approval request
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            approval_file = self.pending_approval / f'LINKEDIN_POST_{timestamp}.md'
            
            approval_content = f"""---
type: approval_request
action: linkedin_post
created: {datetime.now().isoformat()}
status: pending
requires_human_approval: true
source_file: {file_path.name}
topic: {topic}
---

# LinkedIn Post Approval Request ⚠️ HUMAN-IN-THE-LOOP

## Post Details
- **Topic**: {topic}
- **Created**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Post Content
```
{post_content}
```

## Human-in-the-Loop Requirement
This post CANNOT be published without your explicit approval.

### To APPROVE:
1. Review the post content above
2. Check for:
   - Professional tone
   - No typos or errors
   - On-brand messaging
   - Appropriate hashtags (3-5 recommended)
3. Move this file to `/approved/` folder
4. Run: python -m skills.linkedin_poster
5. The poster will publish to LinkedIn automatically

### To REJECT:
1. Move this file to `/rejected/` folder, OR
2. Delete this file
3. Optionally edit and resubmit

## Notes
- All LinkedIn posts require human approval
- This is a production system with HITL enforcement
- Browser automation via Playwright

---
*Created by LinkedIn Watcher (Browser-based)*
*Uses your saved LinkedIn session*
"""
            
            approval_file.write_text(approval_content, encoding='utf-8')
            self.logger.info(f"✓ Approval request created: {approval_file}")
            
            return approval_file
            
        except Exception as e:
            self.logger.error(f"Error creating approval: {e}")
            return None
    
    def run(self):
        """Start watching for LinkedIn posts"""
        print("\n" + "="*70)
        print("📱 LinkedIn Watcher - AI Employee")
        print("="*70)
        print(f"\n📁 Monitoring: {self.needs_action}")
        print(f"⏱️  Interval: {self.check_interval}s")
        print(f"🔒 HITL: All posts require approval")
        
        print("\n" + "="*70)
        print("WORKFLOW:")
        print("1. Create post request in /needs_action/")
        print("2. Watcher creates approval in /pending_approval/")
        print("3. Review and move to /approved/")
        print("4. Run: python -m skills.linkedin_poster")
        print("5. Posted to LinkedIn automatically")
        print("="*70)
        print("\n📡 Starting watcher...\n")
        
        self.logger.info('Starting LinkedInWatcher')
        
        try:
            while True:
                try:
                    # Check for new post requests
                    new_files = self.check_for_updates()
                    for file_path in new_files:
                        self.create_action_file(file_path)
                    
                    # Check for approved posts
                    approved_files = self.check_approved_posts()
                    if approved_files:
                        self.logger.info(f"⚠️  {len(approved_files)} post(s) awaiting posting")
                        self.logger.info("   Run: python -m skills.linkedin_poster")
                    
                except Exception as e:
                    self.logger.error(f"Error during check: {e}")
                
                time.sleep(self.check_interval)
                
        except KeyboardInterrupt:
            self.logger.info("LinkedIn watcher stopped by user")
            print("\n\nStopping LinkedIn Watcher...")
        except Exception as e:
            self.logger.error(f"Error in LinkedIn watcher: {e}")


def main():
    """Main entry point"""
    watcher = LinkedInWatcher(str(project_root), check_interval=30)
    watcher.run()


if __name__ == "__main__":
    main()
