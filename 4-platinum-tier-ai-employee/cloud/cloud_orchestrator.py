"""
Cloud Orchestrator for Platinum Tier AI Employee
Coordinates Cloud watchers, creates drafts (draft-only domain)
Writes to /Updates/ for Local sync
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


class CloudOrchestrator:
    """
    Cloud Orchestrator - Draft-Only Domain
    
    Responsibilities:
    - Read tasks from Cloud watchers
    - Create draft responses (cannot send)
    - Write drafts to /Updates/ for Local sync
    - Track Cloud-processed tasks
    """

    def __init__(self, project_path: str, agent_name: str):
        self.project_path = Path(project_path)
        self.agent_name = agent_name
        
        # Cloud-specific folders
        self.needs_action = self.project_path / 'needs_action'
        self.plans = self.project_path / 'plans'
        self.pending_approval = self.project_path / 'pending_approval'
        self.updates = self.project_path / 'updates'  # Cloud writes here
        self.signals = self.project_path / 'signals'  # Cross-agent signals
        self.done = self.project_path / 'done'
        self.logs = self.project_path / 'logs'

        # Create directories
        for folder in [self.needs_action, self.plans, self.pending_approval,
                       self.updates, self.signals, self.done, self.logs]:
            folder.mkdir(parents=True, exist_ok=True)

        # Setup logging
        self._setup_logging()

        # State tracking
        self.processed_files = set()
        self.current_plan = None

        self.logger.info(f"Cloud Orchestrator initialized ({agent_name})")
        self.logger.info("Domain: Draft-Only (cannot send/post)")

    def _setup_logging(self):
        """Setup logging for the orchestrator"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(self.logs / f'cloud_orchestrator_{datetime.now().strftime("%Y%m%d")}.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(self.__class__.__name__)

    def check_needs_action(self) -> List[Path]:
        """Check for new files in needs_action folder"""
        new_files = []

        for file_path in self.needs_action.glob('*.md'):
            if str(file_path) not in self.processed_files:
                # Check if file is being processed
                plan_exists = any(
                    p.name.startswith(f'PLAN_{file_path.stem}')
                    for p in self.plans.glob('*.md')
                )

                if not plan_exists:
                    new_files.append(file_path)
                    self.processed_files.add(str(file_path))

        return new_files

    def create_draft(self, task_file: Path) -> Dict:
        """
        Create a draft response for a task
        Cloud can ONLY draft - cannot send/post
        """
        try:
            self.logger.info(f"Creating draft for task: {task_file.name}")

            # Read the task file
            content = task_file.read_text(encoding='utf-8')

            # Parse frontmatter
            metadata = self._parse_frontmatter(content)

            # Extract task type
            task_type = metadata.get('type', 'unknown')
            priority = metadata.get('priority', 'medium')

            # Create draft based on task type
            if task_type == 'email':
                draft_result = self._create_email_draft(task_file, content, metadata)
            elif task_type in ['facebook', 'instagram', 'linkedin']:
                draft_result = self._create_social_draft(task_file, content, metadata, task_type)
            else:
                draft_result = self._create_general_draft(task_file, content, metadata)

            if draft_result:
                # Write draft to /Updates/ for Local sync
                self._write_to_updates(draft_result)

            return draft_result

        except Exception as e:
            self.logger.error(f"Error creating draft: {e}")
            return None

    def _create_email_draft(self, task_file: Path, content: str, metadata: dict) -> Dict:
        """Create email draft response"""
        try:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            draft_file = self.updates / f'DRAFT_EMAIL_{timestamp}.md'

            # Extract email details
            from_email = metadata.get('from', 'Unknown')
            subject = metadata.get('subject', 'No Subject')

            # Create draft content
            draft_content = f"""---
type: email_draft
created: {datetime.now().isoformat()}
status: draft
priority: {metadata.get('priority', 'medium')}
source_task: {task_file.name}
created_by: {self.agent_name}
requires_approval: true
---

# Email Draft (Cloud-Generated)

## Original Email
- **From**: {from_email}
- **Subject**: {subject}
- **Received**: {metadata.get('received', 'Unknown')}

## Draft Reply
<!-- Cloud Agent created this draft. Local Agent must review and send. -->

**To**: {from_email}
**Subject**: Re: {subject}

**Body**:

Dear Sender,

[AI-generated response based on email content analysis]

Best regards,
AI Employee

## To Send
1. Review and edit the draft above
2. Move this file to `/approved/` folder
3. Local Agent will execute send

## Notes
- Created by Cloud Agent ({self.agent_name})
- Requires Local approval before sending
- All actions logged for audit
"""

            draft_file.write_text(draft_content, encoding='utf-8')

            self.logger.info(f"Email draft created: {draft_file}")

            return {
                "status": "success",
                "draft_type": "email",
                "draft_file": str(draft_file),
                "source_task": str(task_file),
                "created_by": self.agent_name
            }

        except Exception as e:
            self.logger.error(f"Error creating email draft: {e}")
            return None

    def _create_social_draft(self, task_file: Path, content: str, metadata: dict, platform: str) -> Dict:
        """Create social media post draft"""
        try:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            draft_file = self.updates / f'DRAFT_{platform.upper()}_{timestamp}.md'

            # Generate post content
            post_content = self._generate_social_post_content(content, platform)

            draft_content = f"""---
type: {platform}_draft
created: {datetime.now().isoformat()}
status: draft
priority: medium
source_task: {task_file.name}
created_by: {self.agent_name}
platform: {platform}
requires_approval: true
---

# {platform.title()} Post Draft (Cloud-Generated)

## Post Content
<!-- Cloud Agent created this draft. Local Agent must review and publish. -->

{post_content}

## To Publish
1. Review and edit the content above
2. Move this file to `/approved/` folder
3. Local Agent will execute publish

## Notes
- Created by Cloud Agent ({self.agent_name})
- Requires Local approval before publishing
- All actions logged for audit
"""

            draft_file.write_text(draft_content, encoding='utf-8')

            self.logger.info(f"{platform.title()} draft created: {draft_file}")

            return {
                "status": "success",
                "draft_type": platform,
                "draft_file": str(draft_file),
                "source_task": str(task_file),
                "created_by": self.agent_name
            }

        except Exception as e:
            self.logger.error(f"Error creating social draft: {e}")
            return None

    def _generate_social_post_content(self, content: str, platform: str) -> str:
        """Generate social media post content"""
        # Simple template-based generation
        # In production, Claude would analyze and generate content
        
        templates = {
            'facebook': "📢 Business Update\n\n[Content based on detected event]\n\n#Business #Update",
            'instagram': "✨ Visual Post\n\n[Caption for image]\n\n#InstaPost #Business",
            'linkedin': "💼 Professional Update\n\n[Business-related content]\n\n#Professional #Business"
        }
        
        return templates.get(platform, "[Social media post content]")

    def _create_general_draft(self, task_file: Path, content: str, metadata: dict) -> Dict:
        """Create general draft for unknown task types"""
        try:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            draft_file = self.updates / f'DRAFT_GENERAL_{timestamp}.md'

            draft_content = f"""---
type: general_draft
created: {datetime.now().isoformat()}
status: draft
priority: {metadata.get('priority', 'medium')}
source_task: {task_file.name}
created_by: {self.agent_name}
requires_approval: true
---

# General Draft (Cloud-Generated)

## Source Task
- **File**: {task_file.name}
- **Type**: {metadata.get('type', 'unknown')}
- **Priority**: {metadata.get('priority', 'medium')}

## Draft Action
<!-- Cloud Agent created this draft. Local Agent must review and execute. -->

[Draft action content based on task analysis]

## To Execute
1. Review and edit the content above
2. Move this file to `/approved/` folder
3. Local Agent will execute

## Notes
- Created by Cloud Agent ({self.agent_name})
- Requires Local approval before execution
"""

            draft_file.write_text(draft_content, encoding='utf-8')

            return {
                "status": "success",
                "draft_type": "general",
                "draft_file": str(draft_file),
                "source_task": str(task_file),
                "created_by": self.agent_name
            }

        except Exception as e:
            self.logger.error(f"Error creating general draft: {e}")
            return None

    def _write_to_updates(self, draft_result: dict):
        """Signal that update is ready for Local sync"""
        try:
            signal_file = self.signals / f'UPDATE_READY_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
            
            signal_content = {
                "type": "draft_created",
                "timestamp": datetime.now().isoformat(),
                "created_by": self.agent_name,
                "draft_file": draft_result.get('draft_file'),
                "draft_type": draft_result.get('draft_type')
            }
            
            signal_file.write_text(json.dumps(signal_content, indent=2))
            
            self.logger.info(f"Update signal created: {signal_file}")
            
        except Exception as e:
            self.logger.error(f"Error writing update signal: {e}")

    def check_completed(self) -> List[str]:
        """Check for tasks completed by Local (synced back)"""
        completed = []
        
        # Check /done/ folder for tasks created by Cloud
        for done_file in self.done.glob('*.md'):
            content = done_file.read_text(encoding='utf-8')
            metadata = self._parse_frontmatter(content)
            
            # Check if Cloud created the original draft
            if metadata.get('created_by') == self.agent_name:
                completed.append(done_file.name)
        
        return completed

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

    def create_plan(self, task_file: Path) -> Path:
        """Create a plan file (for Cloud processing)"""
        try:
            content = task_file.read_text(encoding='utf-8')
            metadata = self._parse_frontmatter(content)
            
            task_type = metadata.get('type', 'unknown')
            priority = metadata.get('priority', 'medium')

            plan_content = f"""---
type: cloud_plan
created: {datetime.now().isoformat()}
status: processing
priority: {priority}
task_type: {task_type}
source_file: {task_file.name}
created_by: {self.agent_name}
---

# Cloud Plan: {task_type.title()} Processing

## Objective
Create draft response for {task_type} from Cloud Agent.

## Context
- **Source**: {task_file.name}
- **Priority**: {priority}
- **Created**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
- **Agent**: {self.agent_name}

## Steps (Cloud Domain)
- [x] Read and analyze the {task_type} content
- [ ] Create draft response
- [ ] Write to /Updates/ for Local sync
- [ ] Create completion signal

## Notes
Cloud Agent can only draft - Local Agent must approve and execute.

"""

            plan_filename = f'PLAN_CLOUD_{task_file.stem}_{datetime.now().strftime("%Y%m%d_%H%M%S")}.md'
            plan_path = self.plans / plan_filename
            plan_path.write_text(plan_content, encoding='utf-8')

            self.logger.info(f"Cloud plan created: {plan_path}")
            self.current_plan = plan_path

            return plan_path

        except Exception as e:
            self.logger.error(f"Error creating plan: {e}")
            return None

    def process_with_claude(self, plan_file: Path) -> bool:
        """Process plan with Claude (creates draft)"""
        try:
            self.logger.info(f"Processing Cloud plan with Claude: {plan_file}")

            # Read plan to get source file
            plan_content = plan_file.read_text(encoding='utf-8')
            metadata = self._parse_frontmatter(plan_content)
            source_file = metadata.get('source_file', '')

            # Find source file
            source_path = self.needs_action / source_file
            if not source_path.exists():
                self.logger.warning(f"Source file not found: {source_path}")
                return False

            # Create draft
            draft_result = self.create_draft(source_path)

            return draft_result is not None

        except Exception as e:
            self.logger.error(f"Error processing with Claude: {e}")
            return False
