"""
Cloud Watchers for Platinum Tier AI Employee
API-based watchers that run 24/7 on Railway
Draft-Only Domain: Gmail, Facebook, Instagram
"""
import os
import sys
import time
import logging
import threading
from pathlib import Path
from datetime import datetime
from typing import List

# Add the project root to the Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from watchers.gmail_watcher import GmailWatcher
from watchers.facebook_watcher import FacebookWatcher
from watchers.instagram_watcher import InstagramWatcher


class CloudWatcherManager:
    """
    Manages Cloud watchers (API-based only)
    
    Cloud watchers:
    - Gmail Watcher (API) - detects emails
    - Facebook Watcher (API) - detects events
    - Instagram Watcher (API) - detects events
    
    Cloud CANNOT run:
    - WhatsApp (requires browser session)
    - LinkedIn (requires browser automation)
    """

    def __init__(self, project_path: str, agent_name: str):
        self.project_path = Path(project_path)
        self.agent_name = agent_name
        self.running = False
        
        # Setup logging
        self._setup_logging()
        
        # Initialize Cloud watchers (API-based only)
        self._initialize_watchers()
        
        self.logger.info(f"Cloud Watcher Manager initialized ({agent_name})")

    def _setup_logging(self):
        """Setup logging"""
        log_dir = self.project_path / 'logs'
        log_dir.mkdir(exist_ok=True)

        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_dir / f'cloud_watchers_{datetime.now().strftime("%Y%m%d")}.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(self.__class__.__name__)

    def _initialize_watchers(self):
        """Initialize Cloud watchers"""
        project_path_str = str(self.project_path)
        
        # Gmail Watcher (API-based)
        self.gmail_watcher = GmailWatcher(
            project_path_str,
            check_interval=120
        )
        self.logger.info("Gmail Watcher initialized")
        
        # Facebook Watcher (API-based)
        self.facebook_watcher = FacebookWatcher(
            project_path_str,
            check_interval=120
        )
        self.logger.info("Facebook Watcher initialized")
        
        # Instagram Watcher (API-based)
        self.instagram_watcher = InstagramWatcher(
            project_path_str,
            check_interval=120
        )
        self.logger.info("Instagram Watcher initialized")
        
        # Note: Cloud CANNOT run WhatsApp or LinkedIn watchers
        # (require browser automation/sessions)
        self.logger.info("Note: WhatsApp and LinkedIn watchers disabled on Cloud")

    def run(self):
        """Run all Cloud watchers in threads"""
        self.logger.info("Starting Cloud Watchers...")
        self.running = True
        
        # Start Gmail watcher thread
        self.gmail_thread = threading.Thread(
            target=self.gmail_watcher.run,
            daemon=True,
            name="CloudGmailWatcher"
        )
        self.gmail_thread.start()
        
        # Start Facebook watcher thread
        self.facebook_thread = threading.Thread(
            target=self.facebook_watcher.run,
            daemon=True,
            name="CloudFacebookWatcher"
        )
        self.facebook_thread.start()
        
        # Start Instagram watcher thread
        self.instagram_thread = threading.Thread(
            target=self.instagram_watcher.run,
            daemon=True,
            name="CloudInstagramWatcher"
        )
        self.instagram_thread.start()
        
        self.logger.info("All Cloud Watchers started")
        
        # Keep running
        while self.running:
            time.sleep(60)

    def stop(self):
        """Stop all Cloud watchers"""
        self.logger.info("Stopping Cloud Watchers...")
        self.running = False
        
        # Watchers will stop when their threads exit
        self.logger.info("Cloud Watchers stopped")


class CloudGmailWatcher(GmailWatcher):
    """
    Cloud-specific Gmail watcher
    Overrides to mark emails as Cloud-processed
    """
    
    def __init__(self, project_path: str, agent_name: str, check_interval: int = 120):
        super().__init__(project_path, check_interval)
        self.agent_name = agent_name
        self.logger.info(f"Cloud Gmail Watcher initialized ({agent_name})")
    
    def create_action_file(self, message) -> Path:
        """Create action file with Cloud metadata"""
        filepath = super().create_action_file(message)
        
        if filepath:
            # Add Cloud agent metadata
            content = filepath.read_text(encoding='utf-8')
            content = content.replace(
                'status: pending',
                f'status: pending\ndetected_by: {self.agent_name}'
            )
            filepath.write_text(content, encoding='utf-8')
        
        return filepath


class CloudFacebookWatcher(FacebookWatcher):
    """Cloud-specific Facebook watcher"""
    
    def __init__(self, project_path: str, agent_name: str, check_interval: int = 120):
        super().__init__(project_path, check_interval)
        self.agent_name = agent_name
        self.logger.info(f"Cloud Facebook Watcher initialized ({agent_name})")
    
    def create_action_file(self, item) -> Path:
        """Create action file with Cloud metadata"""
        filepath = super().create_action_file(item)
        
        if filepath:
            content = filepath.read_text(encoding='utf-8')
            content = content.replace(
                'status: pending',
                f'status: pending\ndetected_by: {self.agent_name}'
            )
            filepath.write_text(content, encoding='utf-8')
        
        return filepath


class CloudInstagramWatcher(InstagramWatcher):
    """Cloud-specific Instagram watcher"""
    
    def __init__(self, project_path: str, agent_name: str, check_interval: int = 120):
        super().__init__(project_path, check_interval)
        self.agent_name = agent_name
        self.logger.info(f"Cloud Instagram Watcher initialized ({agent_name})")
    
    def create_action_file(self, item) -> Path:
        """Create action file with Cloud metadata"""
        filepath = super().create_action_file(item)
        
        if filepath:
            content = filepath.read_text(encoding='utf-8')
            content = content.replace(
                'status: pending',
                f'status: pending\ndetected_by: {self.agent_name}'
            )
            filepath.write_text(content, encoding='utf-8')
        
        return filepath
