"""
LinkedIn Watcher for Gold Tier AI Employee
Monitors LinkedIn messages and notifications using Playwright
"""
import time
import logging
from pathlib import Path
from datetime import datetime
from typing import List, Dict
import sys

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


class LinkedInWatcher:
    """
    LinkedIn Watcher - Monitors LinkedIn messages and notifications
    Uses Playwright browser automation
    """

    def __init__(self, project_path: str = None, check_interval: int = 120):
        if project_path is None:
            self.project_path = project_root
        else:
            self.project_path = Path(project_path)

        self.needs_action = self.project_path / 'needs_action'
        self.session_path = self.project_path / 'sessions' / 'linkedin'
        self.check_interval = check_interval
        self.processed_items = set()

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
        self.session_path.mkdir(parents=True, exist_ok=True)

        self.logger.info("LinkedIn Watcher initialized")

    def check_for_updates(self) -> List[Dict]:
        """Check for new LinkedIn messages using Playwright"""
        try:
            from playwright.sync_api import sync_playwright

            self.logger.info("Opening browser to check LinkedIn messages...")

            pw = sync_playwright().start()
            ctx = pw.chromium.launch_persistent_context(
                str(self.session_path),
                headless=False,
                args=['--no-sandbox']
            )
            page = ctx.pages[0] if ctx.pages else ctx.new_page()

            # Go to LinkedIn messaging
            page.goto('https://www.linkedin.com/messaging/', wait_until='domcontentloaded', timeout=180000)

            # Give user time to log in if needed (30 seconds)
            self.logger.info("Waiting 30 seconds for page to load...")
            time.sleep(30)

            # Check if logged in
            if 'login' in page.url.lower() or 'authwall' in page.url.lower():
                self.logger.warning("Not logged in to LinkedIn. Please log in manually.")
                ctx.close()
                pw.stop()
                return []

            messages = []

            # Try to find unread messages
            try:
                # Look for unread message indicators
                unread_convos = page.locator('[class*="msg-conversation-card--unread"]').all()[:5]

                if len(unread_convos) > 0:
                    self.logger.info(f"Found {len(unread_convos)} unread conversations")

                    for convo in unread_convos:
                        try:
                            text = convo.inner_text()
                            item_hash = hash(text[:100])

                            if item_hash not in self.processed_items:
                                messages.append({
                                    'id': f'li_msg_{int(time.time())}_{item_hash}',
                                    'text': text[:500],
                                    'type': 'message',
                                    'timestamp': datetime.now().isoformat()
                                })
                                self.processed_items.add(item_hash)
                        except:
                            continue
                else:
                    self.logger.info("No unread messages found")

            except Exception as e:
                self.logger.error(f"Error finding messages: {e}")

            ctx.close()
            pw.stop()

            return messages

        except ImportError:
            self.logger.error("Playwright not installed. Run: pip install playwright && playwright install chromium")
            return []
        except Exception as e:
            self.logger.error(f"Error checking LinkedIn messages: {e}")
            return []

    def create_action_file(self, message: Dict) -> Path:
        """Create action file for LinkedIn message"""
        try:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"LINKEDIN_MESSAGE_{message['id']}_{timestamp}.md"
            file_path = self.needs_action / filename

            content = f"""---
type: linkedin_message
message_id: {message['id']}
received: {message['timestamp']}
status: pending
---

# LinkedIn Message Received

## Message Details
- **Type**: {message['type']}
- **Received**: {message['timestamp']}

## Message Content
{message['text']}

## Suggested Actions
- [ ] Read and understand the message
- [ ] Draft a response if needed
- [ ] Take any required actions
- [ ] Mark as processed
"""

            file_path.write_text(content, encoding='utf-8')
            self.logger.info(f"Created action file: {filename}")

            return file_path

        except Exception as e:
            self.logger.error(f"Error creating action file: {e}")
            return None

    def run(self):
        """Main watcher loop"""
        self.logger.info("Starting LinkedInWatcher")

        while True:
            try:
                messages = self.check_for_updates()

                if messages:
                    self.logger.info(f"Found {len(messages)} new messages")
                    for message in messages:
                        self.create_action_file(message)

                time.sleep(self.check_interval)

            except KeyboardInterrupt:
                self.logger.info("LinkedIn watcher stopped by user")
                break
            except Exception as e:
                self.logger.error(f"Error in LinkedIn watcher loop: {e}")
                time.sleep(self.check_interval)


if __name__ == "__main__":
    watcher = LinkedInWatcher(str(project_root), check_interval=120)
    watcher.run()

