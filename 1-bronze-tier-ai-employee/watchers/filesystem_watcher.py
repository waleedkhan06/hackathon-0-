"""
File System Watcher for AI Employee Bronze Tier
Monitors the inbox folder for new files and creates action items
"""
import time
import logging
from pathlib import Path
from datetime import datetime
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import sys
from pathlib import Path

# Add the project root to the Python path to import BaseWatcher
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from watchers.base_watcher import BaseWatcher


class InboxHandler(FileSystemEventHandler):
    """Handles file system events in the inbox folder"""
    def __init__(self, project_path: str, needs_action_path: str = None):
        self.project_path = Path(project_path)
        if needs_action_path:
            self.needs_action = Path(needs_action_path)
        else:
            self.needs_action = self.project_path / 'needs_action'
        self.logger = logging.getLogger(self.__class__.__name__)
        self.processed_files = set()

    def on_created(self, event):
        self.logger.info(f"File event detected: {event} (is_directory: {event.is_directory})")
        if event.is_directory:
            self.logger.info("Ignoring directory event")
            return

        file_path = Path(event.src_path)
        self.logger.info(f"Processing file: {file_path} with extension: {file_path.suffix.lower()}")

        if file_path.suffix.lower() in ['.txt', '.md', '.pdf', '.docx', '.csv']:
            self.logger.info(f"File extension {file_path.suffix.lower()} is supported")
            if str(file_path) not in self.processed_files:
                self.processed_files.add(str(file_path))
                self.logger.info(f"New file detected and will be processed: {file_path}")
                self.process_file(file_path)
            else:
                self.logger.info(f"File already processed: {file_path}")
        else:
            self.logger.info(f"File extension {file_path.suffix.lower()} is not supported, ignoring")

    def on_moved(self, event):
        if event.is_directory:
            return

        file_path = Path(event.dest_path)
        if file_path.suffix.lower() in ['.txt', '.md', '.pdf', '.docx', '.csv']:
            if str(file_path) not in self.processed_files:
                self.processed_files.add(str(file_path))
                self.logger.info(f"File moved to inbox: {file_path}")
                self.process_file(file_path)

    def process_file(self, file_path: Path):
        """Process the detected file and create an action item"""
        try:
            # Create metadata for the file
            file_stat = file_path.stat()
            metadata = {
                'original_path': str(file_path),
                'original_name': file_path.name,
                'size': file_stat.st_size,
                'created': datetime.fromtimestamp(file_stat.st_ctime).isoformat(),
                'modified': datetime.fromtimestamp(file_stat.st_mtime).isoformat(),
                'extension': file_path.suffix,
                'type': 'file_drop'
            }

            # Create action file in needs_action folder
            action_filename = f"FILE_{file_path.stem}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
            action_file_path = self.needs_action / action_filename

            action_content = f"""---
type: file_drop
original_name: {metadata['original_name']}
size: {metadata['size']} bytes
date_added: {metadata['created']}
status: pending
priority: medium
---

# New File Detected

## File Information
- **Name**: {metadata['original_name']}
- **Size**: {metadata['size']} bytes
- **Type**: {metadata['extension']}
- **Added**: {metadata['created']}

## Original Path
```
{metadata['original_path']}
```

## Recommended Actions
- [ ] Review file content
- [ ] Determine appropriate action
- [ ] Process or delegate as needed

## File Preview (First 500 chars)
```
{self.get_file_preview(file_path)}
```
"""

            action_file_path.write_text(action_content)
            self.logger.info(f"Action file created: {action_file_path}")

        except Exception as e:
            self.logger.error(f"Error processing file {file_path}: {e}")

    def get_file_preview(self, file_path: Path) -> str:
        """Get a preview of the file content (for text files)"""
        try:
            if file_path.suffix.lower() in ['.txt', '.md', '.csv']:
                content = file_path.read_text(encoding='utf-8')
                return content[:500]  # Return first 500 characters
            else:
                return f"[Binary file of type {file_path.suffix}]"
        except Exception:
            return "[Could not read file preview]"


class FileSystemWatcher(BaseWatcher):
    """Watches the inbox folder for new files"""
    def __init__(self, project_path: str, check_interval: int = 10):
        super().__init__(project_path, check_interval)
        self.inbox_path = self.project_path / 'inbox'
        self.observer = Observer()
        self.handler = InboxHandler(str(self.project_path), str(self.needs_action))

        # Create inbox directory if it doesn't exist
        self.inbox_path.mkdir(exist_ok=True)

    def check_for_updates(self) -> list:
        """This method is not used in this implementation since we use watchdog"""
        return []

    def create_action_file(self, item) -> Path:
        """This method is not used in this implementation since we use watchdog"""
        return Path()

    def run(self):
        """Start watching the inbox folder"""
        self.logger.info(f'Starting {self.__class__.__name__}')
        self.logger.info(f'Watching folder: {self.inbox_path}')

        try:
            # Schedule the event handler
            self.observer.schedule(self.handler, str(self.inbox_path), recursive=False)
            self.observer.start()

            self.logger.info("Observer started, waiting for file events...")

            # Keep the main thread alive - this is essential for the watchdog to work
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            self.logger.info("File system watcher stopped by user")
        except Exception as e:
            self.logger.error(f"Error in file system watcher: {e}")
        finally:
            self.observer.stop()
            self.observer.join()