"""
AI Employee Platinum Tier - Cloud Agent
24/7 Always-On deployment on Railway
Draft-Only Domain: Email triage, Social media drafts
"""
import os
import sys
import signal
import threading
import logging
from pathlib import Path
from datetime import datetime
import time

# Add the project root to the Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from cloud.cloud_orchestrator import CloudOrchestrator
from cloud.cloud_watchers import CloudWatcherManager
from sync.vault_sync import VaultSync
from skills.audit_logger import AuditLogger


class CloudAgent:
    """
    Cloud Agent for Platinum Tier AI Employee
    
    Responsibilities:
    - Email triage (draft replies only)
    - Social media draft posts
    - Continuous monitoring via APIs
    - Write drafts to /Updates/ for Local sync
    - NEVER has WhatsApp, Banking, or Payment access
    """

    def __init__(self):
        self.project_path = project_root
        self.running = False
        
        # Initialize components
        self._setup_logging()
        self._initialize_components()
        
        # Register signal handlers
        signal.signal(signal.SIGTERM, self._signal_handler)
        signal.signal(signal.SIGINT, self._signal_handler)
        
        self.logger.info("Cloud Agent initialized")
        self.logger.info(f"Deployment Mode: Cloud (Railway)")
        self.logger.info(f"Agent Name: {self.agent_name}")

    def _setup_logging(self):
        """Setup logging for Cloud Agent"""
        log_dir = self.project_path / 'logs'
        log_dir.mkdir(exist_ok=True)

        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_dir / f'cloud_agent_{datetime.now().strftime("%Y%m%d")}.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(self.__class__.__name__)

    def _initialize_components(self):
        """Initialize all Cloud Agent components"""
        # Get agent configuration
        self.agent_name = os.getenv('CLOUD_AGENT_NAME', 'cloud-primary')
        self.deployment_mode = 'cloud'
        
        # Initialize audit logger
        self.audit_logger = AuditLogger(str(self.project_path))
        
        # Initialize Cloud Orchestrator
        self.orchestrator = CloudOrchestrator(str(self.project_path), self.agent_name)
        
        # Initialize Cloud Watchers
        self.watcher_manager = CloudWatcherManager(str(self.project_path), self.agent_name)
        
        # Initialize Vault Sync (Git-based)
        self.vault_sync = VaultSync(str(self.project_path), self.agent_name)
        
        self.logger.info("All Cloud Agent components initialized")

    def _signal_handler(self, signum, frame):
        """Handle shutdown signals"""
        self.logger.info(f"Received signal {signum}, shutting down Cloud Agent...")
        self.running = False

    def start_watchers(self):
        """Start Cloud watchers in background threads"""
        self.logger.info("Starting Cloud Watchers...")
        
        # Start watcher manager (runs Gmail, Facebook, Instagram watchers)
        self.watcher_thread = threading.Thread(
            target=self.watcher_manager.run,
            daemon=True,
            name="CloudWatchers"
        )
        self.watcher_thread.start()
        
        self.logger.info("Cloud Watchers started")

    def start_sync_loop(self):
        """Start vault sync loop"""
        self.logger.info("Starting Vault Sync Loop...")
        
        self.sync_thread = threading.Thread(
            target=self._run_sync_loop,
            daemon=True,
            name="VaultSync"
        )
        self.sync_thread.start()
        
        self.logger.info("Vault Sync Loop started")

    def _run_sync_loop(self):
        """Run vault sync in a loop"""
        sync_interval = int(os.getenv('SYNC_INTERVAL_SECONDS', '60'))
        
        while self.running:
            try:
                # Pull any Local updates (approvals, completions)
                self.logger.info("Pulling updates from Local...")
                pull_result = self.vault_sync.pull_updates()
                
                if pull_result.get('status') == 'success':
                    self.logger.info(f"Sync pull: {pull_result.get('message')}")
                
                # Push Cloud drafts/updates
                self.logger.info("Pushing Cloud drafts...")
                push_result = self.vault_sync.push_updates()
                
                if push_result.get('status') == 'success':
                    self.logger.info(f"Sync push: {push_result.get('message')}")
                
                # Wait for next sync interval
                time.sleep(sync_interval)
                
            except Exception as e:
                self.logger.error(f"Error in sync loop: {e}")
                self.audit_logger.log(
                    action_type="sync_error",
                    actor=self.agent_name,
                    error=str(e),
                    category=AuditLogger.CATEGORY_SYSTEM
                )
                time.sleep(10)

    def run_orchestrator_loop(self):
        """Run Cloud orchestrator main loop"""
        self.logger.info("Starting Cloud Orchestrator Loop...")
        
        while self.running:
            try:
                # Check for new tasks detected by watchers
                new_tasks = self.orchestrator.check_needs_action()
                
                for task_file in new_tasks:
                    self.logger.info(f"Processing Cloud task: {task_file.name}")
                    
                    # Create draft response (Cloud can only draft)
                    draft_result = self.orchestrator.create_draft(task_file)
                    
                    if draft_result:
                        self.logger.info(f"Draft created: {draft_result.get('draft_file')}")
                
                # Check for Local approvals (synced back)
                completed_tasks = self.orchestrator.check_completed()
                
                for completion in completed_tasks:
                    self.logger.info(f"Task completed by Local: {completion}")
                
                # Log heartbeat
                self.audit_logger.log(
                    action_type="cloud_heartbeat",
                    actor=self.agent_name,
                    result="success",
                    category=AuditLogger.CATEGORY_SYSTEM
                )
                
                time.sleep(10)
                
            except Exception as e:
                self.logger.error(f"Error in orchestrator loop: {e}")
                self.audit_logger.log(
                    action_type="orchestrator_error",
                    actor=self.agent_name,
                    error=str(e),
                    category=AuditLogger.CATEGORY_SYSTEM
                )
                time.sleep(10)

    def start(self):
        """Start the complete Cloud Agent"""
        self.logger.info("=" * 60)
        self.logger.info("Starting AI Employee Platinum Tier - CLOUD AGENT")
        self.logger.info("=" * 60)
        self.logger.info(f"Deployment: Railway (24/7 Always-On)")
        self.logger.info(f"Domain: Draft-Only (Email, Social Media)")
        self.logger.info(f"Agent Name: {self.agent_name}")
        self.logger.info("=" * 60)
        
        self.running = True
        
        # Log startup
        self.audit_logger.log(
            action_type="cloud_agent_startup",
            actor=self.agent_name,
            result="success",
            category=AuditLogger.CATEGORY_SYSTEM
        )
        
        # Start all components
        self.start_watchers()
        self.start_sync_loop()
        
        # Run orchestrator loop (blocking)
        try:
            self.run_orchestrator_loop()
        except KeyboardInterrupt:
            self.logger.info("Received keyboard interrupt")
        
        # Shutdown
        self.stop()

    def stop(self):
        """Stop Cloud Agent gracefully"""
        self.logger.info("Stopping Cloud Agent...")
        self.running = False
        
        # Stop watcher manager
        if hasattr(self, 'watcher_manager'):
            self.watcher_manager.stop()
        
        # Log shutdown
        self.audit_logger.log(
            action_type="cloud_agent_shutdown",
            actor=self.agent_name,
            result="success",
            category=AuditLogger.CATEGORY_SYSTEM
        )
        
        self.logger.info("Cloud Agent stopped")


def main():
    """Main entry point for Cloud Agent"""
    print("=" * 60)
    print("AI Employee Platinum Tier - CLOUD AGENT")
    print("=" * 60)
    print("Deployment: Railway (24/7 Always-On)")
    print("Domain: Draft-Only (Email, Social Media)")
    print("Press Ctrl+C to stop\n")
    
    agent = CloudAgent()
    agent.start()


if __name__ == "__main__":
    main()
