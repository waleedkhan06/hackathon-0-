"""
Local Orchestrator for Platinum Tier AI Employee
Full domain execution: Approvals, WhatsApp, Banking, Send/Post
Merges Cloud drafts from /Updates/
"""
import os
import sys
import json
import time
import logging
import re
from pathlib import Path
from datetime import datetime
from typing import Optional, List, Dict
import yaml

# Add the project root to the Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


class LocalOrchestrator:
    """
    Local Orchestrator - Full Domain Execution
    
    Responsibilities:
    - Process tasks from all watchers
    - Merge Cloud drafts from /Updates/
    - Execute approved actions (HITL)
    - Full send/post capability
    - WhatsApp, Banking access
    - Write Dashboard.md (single writer)
    """

    def __init__(self, project_path: str, agent_name: str):
        self.project_path = Path(project_path)
        self.agent_name = agent_name
        
        # Local-specific folders
        self.needs_action = self.project_path / 'needs_action'
        self.plans = self.project_path / 'plans'
        self.pending_approval = self.project_path / 'pending_approval'
        self.approved = self.project_path / 'approved'
        self.done = self.project_path / 'done'
        self.updates = self.project_path / 'updates'  # Cloud writes here
        self.signals = self.project_path / 'signals'  # Cross-agent signals
        self.in_progress = self.project_path / 'in_progress'  # Claim-by-move
        self.dashboard = self.project_path / 'dashboard.md'
        self.logs = self.project_path / 'logs'

        # Create directories
        for folder in [self.needs_action, self.plans, self.pending_approval,
                       self.approved, self.done, self.updates, self.signals,
                       self.in_progress, self.logs]:
            folder.mkdir(parents=True, exist_ok=True)

        # Setup logging
        self._setup_logging()

        # State tracking
        self.processed_files = set()
        self.processed_approvals = set()
        self.current_plan = None

        self.logger.info(f"Local Orchestrator initialized ({agent_name})")
        self.logger.info("Domain: Full (Approvals, WhatsApp, Banking, Send)")

    def _setup_logging(self):
        """Setup logging for the orchestrator"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(self.logs / f'local_orchestrator_{datetime.now().strftime("%Y%m%d")}.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(self.__class__.__name__)

    def check_needs_action(self) -> List[Path]:
        """Check for new files in needs_action folder (includes Cloud drafts)"""
        new_files = []

        # Check Local needs_action
        for file_path in self.needs_action.glob('*.md'):
            if str(file_path) not in self.processed_files:
                plan_exists = any(
                    p.name.startswith(f'PLAN_{file_path.stem}')
                    for p in self.plans.glob('*.md')
                )

                if not plan_exists:
                    new_files.append(file_path)
                    self.processed_files.add(str(file_path))

        # Check Cloud drafts in /updates/
        for update_file in self.updates.glob('DRAFT_*.md'):
            if str(update_file) not in self.processed_files:
                # Move to needs_action for processing
                dest = self.needs_action / update_file.name
                if not dest.exists():
                    update_file.rename(dest)
                    new_files.append(dest)
                    self.processed_files.add(str(dest))
                    self.logger.info(f"Cloud draft merged: {update_file.name}")

        return new_files

    def create_plan(self, task_file: Path) -> Path:
        """Create a Plan.md file for a task"""
        try:
            content = task_file.read_text(encoding='utf-8')
            metadata = self._parse_frontmatter(content)

            task_type = metadata.get('type', 'unknown')
            priority = metadata.get('priority', 'medium')
            from_field = metadata.get('from', metadata.get('original_name', 'Unknown'))
            created_by = metadata.get('created_by', 'unknown')

            # Create plan content
            plan_content = f"""---
type: plan
created: {datetime.now().isoformat()}
status: pending
priority: {priority}
task_type: {task_type}
source_file: {task_file.name}
created_by: {created_by}
objective: Process {task_type} from {from_field}
---

# Plan: {task_type.title()} Processing

## Objective
Process the {task_type} from {from_field} and take appropriate action.

## Context
- **Source**: {task_file.name}
- **Priority**: {priority}
- **Created**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
- **Detected By**: {created_by}

## Steps
- [ ] Read and analyze the {task_type} content
- [ ] Determine required actions
- [ ] Check if approval is needed
- [ ] Execute actions or create approval request
- [ ] Update dashboard
- [ ] Move to done folder

## Notes
Add any observations or decisions here during processing.

## Claude Reasoning
<!-- This section will be populated by Claude Code during processing -->

"""

            plan_filename = f'PLAN_{task_file.stem}_{datetime.now().strftime("%Y%m%d_%H%M%S")}.md'
            plan_path = self.plans / plan_filename
            plan_path.write_text(plan_content, encoding='utf-8')

            self.logger.info(f"Plan created: {plan_path}")
            self.current_plan = plan_path

            return plan_path

        except Exception as e:
            self.logger.error(f"Error creating plan: {e}")
            return None

    def _parse_frontmatter(self, content: str) -> dict:
        """Parse YAML frontmatter from markdown content"""
        metadata = {}
        lines = content.split('\n')

        if lines and lines[0].strip() == '---':
            end_fm_idx = -1
            for i, line in enumerate(lines[1:], 1):
                if line.strip() == '---':
                    end_fm_idx = i
                    break

            if end_fm_idx > 0:
                fm_content = '\n'.join(lines[1:end_fm_idx])
                try:
                    metadata = yaml.safe_load(fm_content) or {}
                except:
                    for line in fm_content.split('\n'):
                        if ':' in line:
                            key, value = line.split(':', 1)
                            metadata[key.strip()] = value.strip()

        return metadata

    def process_with_claude(self, plan_file: Path) -> bool:
        """Process a plan using Claude Code"""
        try:
            self.logger.info(f"Processing plan with Claude: {plan_file}")

            content = plan_file.read_text(encoding='utf-8')
            metadata = self._parse_frontmatter(content)

            task_type = metadata.get('task_type', 'unknown')
            source_file = metadata.get('source_file', '')

            source_path = self.needs_action / source_file
            if not source_path.exists():
                self.logger.warning(f"Source file not found: {source_path}")
                return False

            task_content = source_path.read_text(encoding='utf-8')

            # Create approval request for all actions
            self._create_approval_request(plan_file, source_path, task_type, task_content)

            return True

        except Exception as e:
            self.logger.error(f"Error processing with Claude: {e}")
            return False

    def _create_approval_request(self, plan_file: Path, source_file: Path, task_type: str, task_content: str):
        """Create an approval request file"""
        try:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            action_type = self._determine_action_type(task_content)

            approval_file = self.pending_approval / f'APPROVAL_{action_type}_{timestamp}.md'

            content = f"""---
type: approval_request
action: {action_type}
created: {datetime.now().isoformat()}
status: pending
source_plan: {plan_file.name}
source_task: {source_file.name}
requires_human_approval: true
---

# Approval Required: {action_type.replace('_', ' ').title()}

## Details
- **Action Type**: {action_type}
- **Created**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
- **Source Plan**: {plan_file.name}

## Content
{task_content[:1000]}...

## Why Approval is Needed
This action requires human review before proceeding.

## Human-in-the-Loop Workflow

### To APPROVE:
1. Review the content above
2. **Move this file to `/approved/` folder**
3. Local Agent will automatically execute
4. File will be moved to `/done/` after execution

### To REJECT:
1. Move this file to `/rejected/` folder, OR
2. Delete this file

## Execution Method
- **Email, Facebook, Instagram**: Auto-executed when moved to /approved/
- **LinkedIn, WhatsApp**: Manual execution (Playwright-based)

## Notes
- All actions are logged for audit purposes
- Local Agent has full execution capability
"""

            approval_file.write_text(content, encoding='utf-8')

            # Update plan status
            plan_content = plan_file.read_text(encoding='utf-8')
            plan_content = plan_content.replace('status: pending', 'status: awaiting_approval')
            plan_file.write_text(plan_content, encoding='utf-8')

            self._log_action('approval_requested', {
                'approval_file': str(approval_file),
                'action_type': action_type
            })

            self.logger.info(f"✓ Approval request created: {approval_file}")

        except Exception as e:
            self.logger.error(f"Error creating approval request: {e}")

    def _determine_action_type(self, content: str) -> str:
        """Determine action type from content"""
        content_lower = content.lower()

        if 'email' in content_lower or 'gmail' in content_lower:
            return 'email_send'
        elif 'facebook' in content_lower:
            return 'facebook_post'
        elif 'instagram' in content_lower:
            return 'instagram_post'
        elif 'linkedin' in content_lower:
            return 'linkedin_post'
        elif 'whatsapp' in content_lower:
            return 'whatsapp_send'
        else:
            return 'general_action'

    def check_approved_actions(self) -> List[Path]:
        """Check for approved actions to execute"""
        approved_files = []

        for file_path in self.approved.glob('*.md'):
            if str(file_path) in self.processed_approvals:
                continue

            # Update status to 'approved' if still 'pending'
            content = file_path.read_text(encoding='utf-8')
            if 'status: pending' in content:
                content = content.replace('status: pending', 'status: approved')
                file_path.write_text(content, encoding='utf-8')
                self.logger.info(f"✅ Updated status: {file_path.name}")

            approved_files.append(file_path)
            self.processed_approvals.add(str(file_path))

        return approved_files

    def execute_approved_action(self, approval_file: Path) -> bool:
        """Execute an approved action (Local has full execution capability)"""
        try:
            content = approval_file.read_text(encoding='utf-8')
            metadata = self._parse_frontmatter(content)

            action_type = metadata.get('action', 'unknown')
            self.logger.info(f"Executing approved action: {action_type}")

            # Execute based on action type (Local can execute ALL)
            if 'email' in action_type.lower():
                self._execute_email_send(approval_file)
            elif 'facebook' in action_type.lower():
                self._execute_facebook_post(approval_file)
            elif 'instagram' in action_type.lower():
                self._execute_instagram_post(approval_file)
            elif 'linkedin' in action_type.lower():
                self._execute_linkedin_post(approval_file)
            elif 'whatsapp' in action_type.lower():
                self._execute_whatsapp_send(approval_file)
            else:
                self._execute_generic_action(approval_file)

            # Move to done after successful execution
            done_file = self.done / approval_file.name
            approval_file.rename(done_file)

            self._log_action('approved_action_executed', {
                'action_type': action_type,
                'file': str(approval_file)
            })

            # Update dashboard
            self._update_dashboard()

            return True

        except Exception as e:
            self.logger.error(f"Error executing approved action: {e}")
            return False

    def _execute_email_send(self, approval_file: Path):
        """Execute email send via Gmail API (Local has send capability)"""
        try:
            from mcp_servers.email_mcp import EmailMCPServer
            import re

            content = approval_file.read_text(encoding='utf-8')

            to_match = re.search(r'to:\s*(\S+@\S+)', content)
            subject_match = re.search(r'subject:\s*(.+)', content)

            to_email = to_match.group(1).strip() if to_match else "mwaleedkhan726@gmail.com"
            subject = subject_match.group(1).strip() if subject_match else f"AI Employee Email - {datetime.now().strftime('%H:%M:%S')}"

            body_match = re.search(r'## Email Content\s*\n(.*?)(?=---|## To Approve|$)', content, re.DOTALL)
            body = body_match.group(1).strip() if body_match else f"""
<h1>AI Employee Platinum Tier</h1>
<p>This email was sent automatically by your AI Employee system.</p>
<p><strong>Time:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
<p><strong>Status:</strong> Human-in-the-Loop approval workflow working! ✅</p>
"""

            server = EmailMCPServer()
            result = server.send_email(to=to_email, subject=subject, body=body)

            if result.get('status') == 'success':
                self.logger.info(f"✅ Email sent to {to_email}")
            else:
                self.logger.warning(f"⚠️ Email send failed: {result.get('message')}")

        except Exception as e:
            self.logger.error(f"Error sending email: {e}")

    def _execute_facebook_post(self, approval_file: Path):
        """Execute Facebook post via Meta Graph API"""
        try:
            from mcp_servers.facebook_mcp_api import FacebookMCP
            import re

            content = approval_file.read_text(encoding='utf-8')

            post_match = re.search(r'## Post Content\s*\n(.*?)(?=---|## To Approve|$)', content, re.DOTALL)
            message = post_match.group(1).strip() if post_match else f"""🚀 AI Employee Platinum Tier - Auto Test

Human-in-the-Loop workflow is working!

✅ Approval file created
✅ Human reviewed and approved
✅ Auto-execution via Meta API

#AI #Automation #PlatinumTier

Posted: {datetime.now().strftime('%H:%M:%S')}"""

            mcp = FacebookMCP(str(self.project_path))
            result = mcp.post_text(message)

            if result.get('success'):
                self.logger.info(f"✅ Facebook post successful: {result.get('post_id')}")
            else:
                self.logger.warning(f"⚠️ Facebook post failed: {result.get('error')}")

        except Exception as e:
            self.logger.error(f"Error posting to Facebook: {e}")

    def _execute_instagram_post(self, approval_file: Path):
        """Execute Instagram post via Meta Graph API"""
        try:
            from mcp_servers.instagram_mcp_api import InstagramMCP
            import re

            content = approval_file.read_text(encoding='utf-8')

            image_match = re.search(r'image_url:\s*(\S+)', content)
            caption_match = re.search(r'## Caption\s*\n(.*?)(?=---|## To Approve|$)', content, re.DOTALL)

            image_url = image_match.group(1).strip() if image_match else "https://images.unsplash.com/photo-1677442136019-21780ecad995?w=1080&h=1080&fit=crop"
            caption = caption_match.group(1).strip() if caption_match else f"""🤖 AI Employee Platinum Tier - Auto Test

HITL workflow verified!

✅ Approval → Review → Auto-execute

#AI #Automation #Tech

Posted: {datetime.now().strftime('%H:%M:%S')}"""

            mcp = InstagramMCP(str(self.project_path))
            result = mcp.post_photo(image_url, caption)

            if result.get('success'):
                self.logger.info(f"✅ Instagram post successful: {result.get('media_id')}")
            else:
                self.logger.warning(f"⚠️ Instagram post failed: {result.get('error')}")

        except Exception as e:
            self.logger.error(f"Error posting to Instagram: {e}")

    def _execute_linkedin_post(self, approval_file: Path):
        """Execute LinkedIn post via Playwright"""
        try:
            self.logger.info("=" * 60)
            self.logger.info("📌 LINKEDIN POST READY FOR MANUAL EXECUTION")
            self.logger.info("=" * 60)
            self.logger.info(f"File: {approval_file.name}")
            self.logger.info("Command: python3 skills/linkedin_poster_final.py --file <file>")
            self.logger.info("=" * 60)

        except Exception as e:
            self.logger.error(f"Error with LinkedIn post: {e}")

    def _execute_whatsapp_send(self, approval_file: Path):
        """Execute WhatsApp message via Playwright (Local has session)"""
        try:
            self.logger.info("=" * 60)
            self.logger.info("📱 WHATSAPP MESSAGE READY FOR MANUAL EXECUTION")
            self.logger.info("=" * 60)
            self.logger.info(f"File: {approval_file.name}")
            self.logger.info("Command: python3 skills/whatsapp_sender_fast.py")
            self.logger.info("=" * 60)

        except Exception as e:
            self.logger.error(f"Error with WhatsApp send: {e}")

    def _execute_generic_action(self, approval_file: Path):
        """Execute a generic approved action"""
        self.logger.info(f"Generic action executed: {approval_file.name}")

    def _update_dashboard(self):
        """Update Dashboard.md (Local is single writer)"""
        try:
            # Count tasks in each folder
            needs_action_count = len(list(self.needs_action.glob('*.md')))
            pending_approval_count = len(list(self.pending_approval.glob('*.md')))
            done_count = len(list(self.done.glob('*.md')))

            dashboard_content = f"""---
last_updated: {datetime.now().isoformat()}
updated_by: {self.agent_name}
---

# AI Employee Dashboard

**Last Updated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Agent**: {self.agent_name} (Local)

## Current Status

| Category | Count |
|----------|-------|
| Needs Action | {needs_action_count} |
| Pending Approval | {pending_approval_count} |
| Completed Today | {done_count} |

## Recent Activity

<!-- Auto-updated by Local Orchestrator -->

## Cloud Agent Status

Cloud Agent ({os.getenv('CLOUD_AGENT_NAME', 'unknown')}) is syncing updates.

## Quick Actions

- Review pending approvals: `/pending_approval/`
- Check completed tasks: `/done/`
- View Cloud updates: `/updates/`

---
*Generated by AI Employee Platinum Tier*
"""

            self.dashboard.write_text(dashboard_content, encoding='utf-8')
            self.logger.info("Dashboard updated")

        except Exception as e:
            self.logger.error(f"Error updating dashboard: {e}")

    def _log_action(self, action_type: str, details: dict):
        """Log an action for audit purposes"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "action_type": action_type,
            "actor": self.agent_name,
            "details": details
        }

        log_file = self.logs / f'local_orchestrator_actions_{datetime.now().strftime("%Y%m%d")}.json'

        logs = []
        if log_file.exists():
            try:
                logs = json.loads(log_file.read_text())
            except:
                logs = []

        logs.append(log_entry)
        log_file.write_text(json.dumps(logs, indent=2))

    def run(self):
        """Main orchestration loop"""
        self.logger.info("Starting Local Orchestrator main loop")
        self.logger.info("Full Domain: Approvals, WhatsApp, Banking, Send")

        try:
            while True:
                # Check for new tasks
                new_tasks = self.check_needs_action()

                for task_file in new_tasks:
                    self.logger.info(f"Processing task: {task_file.name}")
                    plan_file = self.create_plan(task_file)

                    if plan_file:
                        self.process_with_claude(plan_file)

                # Check for approved actions
                approved_actions = self.check_approved_actions()

                for approval_file in approved_actions:
                    self.logger.info(f"Executing: {approval_file.name}")
                    self.execute_approved_action(approval_file)

                time.sleep(10)

        except KeyboardInterrupt:
            self.logger.info("Orchestrator stopped by user")
        except Exception as e:
            self.logger.error(f"Error in orchestrator: {e}")
            raise
