"""
Base Watcher Class for AI Employee Bronze Tier
This is a base class that other watchers can inherit from
"""
import time
import logging
from pathlib import Path
from abc import ABC, abstractmethod
import json
from datetime import datetime


class BaseWatcher(ABC):
    def __init__(self, project_path: str, check_interval: int = 60):
        self.project_path = Path(project_path)
        self.needs_action = self.project_path / 'needs_action'
        self.inbox = self.project_path / 'inbox'
        self.check_interval = check_interval

        # Setup logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(self.project_path / 'logs' / f'watcher_{datetime.now().strftime("%Y%m%d")}.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(self.__class__.__name__)

    @abstractmethod
    def check_for_updates(self) -> list:
        """Return list of new items to process"""
        pass

    @abstractmethod
    def create_action_file(self, item) -> Path:
        """Create .md file in needs_action folder"""
        pass

    def run(self):
        self.logger.info(f'Starting {self.__class__.__name__}')
        while True:
            try:
                items = self.check_for_updates()
                for item in items:
                    self.create_action_file(item)
            except Exception as e:
                self.logger.error(f'Error in {self.__class__.__name__}: {e}')
            time.sleep(self.check_interval)