"""
Vault Sync System for Platinum Tier AI Employee
Git-based synchronization between Cloud and Local agents

Sync Rules:
- Cloud writes to /Updates/, /Signals/
- Local merges from /Updates/ to workflow
- Local owns Dashboard.md (single writer)
- Secrets never sync (.env, tokens, sessions)
- Claim-by-move rule for task ownership
"""
import os
import sys
import json
import subprocess
import logging
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, List

# Add the project root to the Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


class VaultSync:
    """
    Git-based vault synchronization
    
    Architecture:
    - Cloud pushes drafts to /Updates/
    - Local pulls from /Updates/ and merges
    - Local pushes completions to /Done/
    - Cloud pulls completions for audit trail
    
    Security:
    - .gitignore excludes .env, tokens, sessions
    - Separate credentials for Cloud and Local
    - Secrets never committed to Git
    """

    def __init__(self, project_path: str, agent_name: str):
        self.project_path = Path(project_path)
        self.agent_name = agent_name
        self.deployment_mode = os.getenv('DEPLOYMENT_MODE', 'local')
        
        # Sync folders
        self.updates = self.project_path / 'updates'
        self.signals = self.project_path / 'signals'
        self.in_progress = self.project_path / 'in_progress'
        self.done = self.project_path / 'done'
        self.logs = self.project_path / 'logs'
        
        # Git configuration
        self.git_dir = self.project_path / '.git'
        self.sync_branch = 'main'
        
        # Create directories
        for folder in [self.updates, self.signals, self.in_progress, self.logs]:
            folder.mkdir(parents=True, exist_ok=True)
        
        # Setup logging
        self._setup_logging()
        
        self.logger.info(f"VaultSync initialized ({agent_name}, {self.deployment_mode})")

    def _setup_logging(self):
        """Setup logging"""
        log_dir = self.project_path / 'logs'
        log_dir.mkdir(exist_ok=True)

        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_dir / f'vault_sync_{datetime.now().strftime("%Y%m%d")}.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(self.__class__.__name__)

    def initialize_git(self, remote_url: str = None) -> Dict:
        """
        Initialize Git repository for vault sync
        
        Args:
            remote_url: Optional Git remote URL
        
        Returns:
            Result of initialization
        """
        try:
            # Check if already initialized
            if not self.git_dir.exists():
                self.logger.info("Initializing Git repository...")
                subprocess.run(
                    ['git', 'init'],
                    cwd=str(self.project_path),
                    capture_output=True,
                    check=True
                )
                self.logger.info("Git repository initialized")
            
            # Configure Git user
            subprocess.run(
                ['git', 'config', 'user.name', f'AI-Employee-{self.agent_name}'],
                cwd=str(self.project_path),
                capture_output=True,
                check=True
            )
            subprocess.run(
                ['git', 'config', 'user.email', f'{self.agent_name}@ai-employee.local'],
                cwd=str(self.project_path),
                capture_output=True,
                check=True
            )
            
            # Add remote if provided
            if remote_url:
                try:
                    subprocess.run(
                        ['git', 'remote', 'remove', 'origin'],
                        cwd=str(self.project_path),
                        capture_output=True
                    )
                except:
                    pass
                
                subprocess.run(
                    ['git', 'remote', 'add', 'origin', remote_url],
                    cwd=str(self.project_path),
                    capture_output=True,
                    check=True
                )
                self.logger.info(f"Remote added: {remote_url}")
            
            # Create .gitignore for secrets isolation
            self._create_gitignore()
            
            return {
                "status": "success",
                "message": "Git repository initialized",
                "git_dir": str(self.git_dir)
            }
            
        except subprocess.CalledProcessError as e:
            self.logger.error(f"Git error: {e.stderr.decode() if e.stderr else str(e)}")
            return {
                "status": "error",
                "message": f"Git initialization failed: {e}"
            }
        except Exception as e:
            self.logger.error(f"Error initializing Git: {e}")
            return {
                "status": "error",
                "message": str(e)
            }

    def _create_gitignore(self):
        """Create .gitignore to exclude secrets"""
        gitignore_content = """# NEVER sync these files - SECURITY CRITICAL
.env
.env.local
.env.cloud
*.env
*.token
*.session
sessions/
secure/
credentials/
keychain/

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
venv/
ENV/
env/

# Logs
logs/*.log
*.log

# OS
.DS_Store
Thumbs.db
desktop.ini

# IDE
.vscode/
.idea/
*.swp
*.swo

# Temporary files
tmp/
temp/
*.tmp
"""
        gitignore_file = self.project_path / '.gitignore'
        gitignore_file.write_text(gitignore_content, encoding='utf-8')
        self.logger.info(".gitignore created (secrets excluded)")

    def pull_updates(self) -> Dict:
        """
        Pull updates from remote repository
        
        Cloud: Pulls Local completions
        Local: Pulls Cloud drafts
        
        Returns:
            Result of pull operation
        """
        try:
            # Check if Git is initialized
            if not self.git_dir.exists():
                return {
                    "status": "error",
                    "message": "Git repository not initialized"
                }
            
            # Fetch from remote
            self.logger.info("Fetching from remote...")
            result = subprocess.run(
                ['git', 'fetch', 'origin'],
                cwd=str(self.project_path),
                capture_output=True,
                text=True
            )
            
            if result.returncode != 0:
                return {
                    "status": "error",
                    "message": f"Fetch failed: {result.stderr}"
                }
            
            # Pull changes (non-interactive, ours strategy for conflicts)
            self.logger.info("Pulling updates...")
            result = subprocess.run(
                ['git', 'pull', '--no-edit', '-X', 'ours'],
                cwd=str(self.project_path),
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                self.logger.info("Pull successful")
                return {
                    "status": "success",
                    "message": "Updates pulled successfully",
                    "output": result.stdout
                }
            else:
                # Handle merge conflicts gracefully
                self.logger.warning(f"Pull had conflicts: {result.stderr}")
                subprocess.run(
                    ['git', 'merge', '--abort'],
                    cwd=str(self.project_path),
                    capture_output=True
                )
                return {
                    "status": "warning",
                    "message": "Pull had conflicts, merged aborted",
                    "output": result.stdout
                }
                
        except Exception as e:
            self.logger.error(f"Error pulling updates: {e}")
            return {
                "status": "error",
                "message": str(e)
            }

    def push_updates(self) -> Dict:
        """
        Push updates to remote repository
        
        Cloud: Pushes drafts to /Updates/
        Local: Pushes completions to /Done/
        
        Returns:
            Result of push operation
        """
        try:
            # Check if Git is initialized
            if not self.git_dir.exists():
                return {
                    "status": "error",
                    "message": "Git repository not initialized"
                }
            
            # Stage changes
            self.logger.info("Staging changes...")
            subprocess.run(
                ['git', 'add', 'updates/', 'signals/'],
                cwd=str(self.project_path),
                capture_output=True
            )
            
            # Check if there are changes to commit
            result = subprocess.run(
                ['git', 'status', '--porcelain'],
                cwd=str(self.project_path),
                capture_output=True,
                text=True
            )
            
            if not result.stdout.strip():
                return {
                    "status": "success",
                    "message": "No changes to push"
                }
            
            # Commit changes
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            subprocess.run(
                ['git', 'commit', '-m', f'{self.agent_name} sync: {timestamp}'],
                cwd=str(self.project_path),
                capture_output=True
            )
            
            # Push to remote
            self.logger.info("Pushing updates...")
            result = subprocess.run(
                ['git', 'push', 'origin', self.sync_branch],
                cwd=str(self.project_path),
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                self.logger.info("Push successful")
                return {
                    "status": "success",
                    "message": "Updates pushed successfully",
                    "output": result.stdout
                }
            else:
                # Handle push rejection (might need pull first)
                if 'rejected' in result.stderr:
                    self.logger.warning("Push rejected, pulling first...")
                    self.pull_updates()
                    
                    # Try push again
                    result = subprocess.run(
                        ['git', 'push', 'origin', self.sync_branch],
                        cwd=str(self.project_path),
                        capture_output=True,
                        text=True
                    )
                    
                    if result.returncode == 0:
                        return {
                            "status": "success",
                            "message": "Updates pushed successfully (after pull)",
                            "output": result.stdout
                        }
                
                return {
                    "status": "error",
                    "message": f"Push failed: {result.stderr}"
                }
                
        except Exception as e:
            self.logger.error(f"Error pushing updates: {e}")
            return {
                "status": "error",
                "message": str(e)
            }

    def push_completions(self) -> Dict:
        """
        Push completed tasks to remote
        
        Local: Pushes /Done/ for Cloud audit trail
        
        Returns:
            Result of push operation
        """
        try:
            if not self.git_dir.exists():
                return {
                    "status": "error",
                    "message": "Git repository not initialized"
                }
            
            # Stage done folder
            subprocess.run(
                ['git', 'add', 'done/'],
                cwd=str(self.project_path),
                capture_output=True
            )
            
            # Check for changes
            result = subprocess.run(
                ['git', 'status', '--porcelain'],
                cwd=str(self.project_path),
                capture_output=True,
                text=True
            )
            
            if not result.stdout.strip():
                return {
                    "status": "success",
                    "message": "No completions to push"
                }
            
            # Commit and push
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            subprocess.run(
                ['git', 'commit', '-m', f'{self.agent_name} completions: {timestamp}'],
                cwd=str(self.project_path),
                capture_output=True
            )
            
            subprocess.run(
                ['git', 'push', 'origin', self.sync_branch],
                cwd=str(self.project_path),
                capture_output=True
            )
            
            self.logger.info("Completions pushed")
            
            return {
                "status": "success",
                "message": "Completions pushed successfully"
            }
            
        except Exception as e:
            self.logger.error(f"Error pushing completions: {e}")
            return {
                "status": "error",
                "message": str(e)
            }

    def merge_updates(self) -> Dict:
        """
        Merge Cloud updates into Local workflow
        
        Local only: Moves Cloud drafts from /Updates/ to /Needs_Action/
        
        Returns:
            Result of merge operation
        """
        if self.deployment_mode == 'cloud':
            return {
                "status": "skipped",
                "message": "Merge only runs on Local agent"
            }
        
        try:
            merged_count = 0
            
            # Move Cloud drafts to needs_action
            for update_file in self.updates.glob('DRAFT_*.md'):
                dest = self.needs_action / update_file.name
                
                if not dest.exists():
                    update_file.rename(dest)
                    merged_count += 1
                    self.logger.info(f"Merged Cloud draft: {update_file.name}")
            
            # Process signals
            for signal_file in self.signals.glob('*.json'):
                signal_content = json.loads(signal_file.read_text())
                
                if signal_content.get('type') == 'draft_created':
                    self.logger.info(f"Cloud signal: {signal_content.get('draft_type')} draft created")
                
                # Archive signal
                archive_dir = self.logs / 'signals_archive'
                archive_dir.mkdir(exist_ok=True)
                signal_file.rename(archive_dir / signal_file.name)
            
            return {
                "status": "success",
                "merged_count": merged_count,
                "message": f"Merged {merged_count} Cloud updates"
            }
            
        except Exception as e:
            self.logger.error(f"Error merging updates: {e}")
            return {
                "status": "error",
                "message": str(e)
            }

    def claim_task(self, task_file: Path) -> Dict:
        """
        Claim a task using claim-by-move rule
        
        First agent to move task to /In_Progress/<agent>/ owns it
        
        Args:
            task_file: Path to task file
        
        Returns:
            Result of claim operation
        """
        try:
            if not task_file.exists():
                return {
                    "status": "error",
                    "message": "Task file not found"
                }
            
            # Create agent-specific in_progress folder
            agent_folder = self.in_progress / self.agent_name
            agent_folder.mkdir(parents=True, exist_ok=True)
            
            # Move task to claim it
            dest = agent_folder / task_file.name
            
            if dest.exists():
                return {
                    "status": "error",
                    "message": "Task already claimed"
                }
            
            task_file.rename(dest)
            
            self.logger.info(f"Task claimed: {task_file.name}")
            
            return {
                "status": "success",
                "message": "Task claimed",
                "claimed_file": str(dest)
            }
            
        except Exception as e:
            self.logger.error(f"Error claiming task: {e}")
            return {
                "status": "error",
                "message": str(e)
            }

    def release_task(self, task_file: Path, destination: str = 'done') -> Dict:
        """
        Release a claimed task after completion
        
        Args:
            task_file: Path to claimed task file
            destination: 'done' or 'needs_action'
        
        Returns:
            Result of release operation
        """
        try:
            if not task_file.exists():
                return {
                    "status": "error",
                    "message": "Task file not found"
                }
            
            if destination == 'done':
                dest = self.done / task_file.name
            elif destination == 'needs_action':
                dest = self.needs_action / task_file.name
            else:
                return {
                    "status": "error",
                    "message": "Invalid destination"
                }
            
            task_file.rename(dest)
            
            self.logger.info(f"Task released to {destination}: {task_file.name}")
            
            return {
                "status": "success",
                "message": f"Task released to {destination}"
            }
            
        except Exception as e:
            self.logger.error(f"Error releasing task: {e}")
            return {
                "status": "error",
                "message": str(e)
            }

    def get_sync_status(self) -> Dict:
        """
        Get current sync status
        
        Returns:
            Sync status information
        """
        try:
            status = {
                "agent_name": self.agent_name,
                "deployment_mode": self.deployment_mode,
                "git_initialized": self.git_dir.exists(),
                "updates_count": len(list(self.updates.glob('*.md'))),
                "signals_count": len(list(self.signals.glob('*.json'))),
                "in_progress_count": sum(
                    1 for f in self.in_progress.rglob('*.md')
                ),
                "done_count": len(list(self.done.glob('*.md')))
            }
            
            if self.git_dir.exists():
                # Get Git status
                result = subprocess.run(
                    ['git', 'status', '--porcelain'],
                    cwd=str(self.project_path),
                    capture_output=True,
                    text=True
                )
                status["pending_changes"] = len(result.stdout.strip().split('\n')) if result.stdout.strip() else 0
            
            return {
                "status": "success",
                "sync_status": status
            }
            
        except Exception as e:
            self.logger.error(f"Error getting sync status: {e}")
            return {
                "status": "error",
                "message": str(e)
            }
