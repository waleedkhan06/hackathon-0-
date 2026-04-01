"""
Instagram Watcher - Monitor Instagram using Meta Graph API
Part of Gold Tier AI Employee Implementation
Uses Meta Graph API for reliable monitoring (no browser automation needed)
"""

import os
import time
import logging
import requests
from pathlib import Path
from datetime import datetime, timedelta
from typing import List, Dict
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class InstagramWatcher:
    """
    Monitors Instagram using Meta Graph API:
    - Comments on media
    - Direct messages (via Instagram Basic Display API)
    - Media engagement
    """

    def __init__(self, vault_path: str, check_interval: int = 300):
        """
        Initialize Instagram Watcher

        Args:
            vault_path: Path to the Obsidian vault
            check_interval: Seconds between checks (default 5 minutes)
        """
        self.vault_path = Path(vault_path)
        self.needs_action = self.vault_path / 'needs_action'
        self.check_interval = check_interval
        self.logger = self._setup_logger()

        # Meta API credentials
        self.ig_account_id = os.getenv('INSTAGRAM_BUSINESS_ACCOUNT_ID')
        self.access_token = os.getenv('INSTAGRAM_ACCESS_TOKEN')

        # Demo mode flag
        self.demo_mode = os.getenv('INSTAGRAM_DEMO_MODE', 'true').lower() == 'true'

        # Validate credentials
        if not self.demo_mode and not all([self.ig_account_id, self.access_token]):
            self.logger.warning("Instagram API credentials not found. Running in demo mode.")
            self.demo_mode = True

        # Track processed items
        self.processed_items = set()
        self.last_check_time = datetime.now() - timedelta(minutes=5)

        # Create required directories
        self.needs_action.mkdir(exist_ok=True)

        if not self.demo_mode:
            self.logger.info(f"Instagram Watcher initialized for account: {self.ig_account_id}")
        else:
            self.logger.info("Instagram Watcher initialized in DEMO mode")

    def _setup_logger(self) -> logging.Logger:
        """Setup logging for the watcher"""
        logger = logging.getLogger('InstagramWatcher')
        logger.setLevel(logging.INFO)

        # Create logs directory if it doesn't exist
        log_dir = self.vault_path / 'logs'
        log_dir.mkdir(exist_ok=True)

        # File handler
        log_file = log_dir / f'instagram_watcher_{datetime.now().strftime("%Y%m%d")}.log'
        fh = logging.FileHandler(log_file)
        fh.setLevel(logging.INFO)

        # Console handler
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)

        # Formatter
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)

        logger.addHandler(fh)
        logger.addHandler(ch)

        return logger

    def check_for_updates(self) -> List[Dict]:
        """Check for new Instagram activity using Meta Graph API"""
        if self.demo_mode:
            return self._demo_check()

        try:
            updates = []

            # Check for new comments on recent media
            comments = self._get_recent_comments()
            updates.extend(comments)

            # Check for new mentions
            mentions = self._get_mentions()
            updates.extend(mentions)

            self.last_check_time = datetime.now()

            return updates

        except Exception as e:
            self.logger.error(f"Error checking Instagram: {e}")
            return []

    def _get_recent_comments(self) -> List[Dict]:
        """Get recent comments on Instagram media"""
        try:
            # Get recent media
            media_url = f"https://graph.facebook.com/v19.0/{self.ig_account_id}/media"
            media_params = {
                'fields': 'id,caption,timestamp,comments.fields(from,text,created_time,hideable)',
                'limit': 5,
                'access_token': self.access_token
            }

            media_response = requests.get(media_url, params=media_params, timeout=30)

            if media_response.status_code != 200:
                self.logger.error(f"Media API error: {media_response.text}")
                return []

            media_data = media_response.json()
            comments = []

            if 'data' in media_data:
                for media in media_data['data']:
                    if 'comments' in media and 'data' in media['comments']:
                        for comment in media['comments']['data']:
                            comment_time = datetime.strptime(
                                comment.get('created_time', ''),
                                '%Y-%m-%dT%H:%M:%S%z'
                            ) if comment.get('created_time') else None

                            # Only get comments since last check
                            if comment_time and comment_time > self.last_check_time:
                                item_hash = hash(f"ig_comment:{comment.get('id')}")

                                if item_hash not in self.processed_items:
                                    comments.append({
                                        'id': comment.get('id'),
                                        'type': 'comment',
                                        'from': comment.get('from', {}).get('username', 'Unknown'),
                                        'message': comment.get('text', ''),
                                        'media_id': media.get('id'),
                                        'media_caption': media.get('caption', '')[:100],
                                        'timestamp': comment.get('created_time'),
                                        'hideable': comment.get('hideable', False)
                                    })
                                    self.processed_items.add(item_hash)
                                    self.logger.info(f"New Instagram comment from @{comment.get('from', {}).get('username', 'Unknown')}")

            return comments

        except Exception as e:
            self.logger.error(f"Error getting Instagram comments: {e}")
            return []

    def _get_mentions(self) -> List[Dict]:
        """Get recent mentions in comments"""
        try:
            # Get recent media
            media_url = f"https://graph.facebook.com/v19.0/{self.ig_account_id}/media"
            media_params = {
                'fields': 'id,caption,comments.fields(from,text,created_time)',
                'limit': 10,
                'access_token': self.access_token
            }

            media_response = requests.get(media_url, params=media_params, timeout=30)

            if media_response.status_code != 200:
                self.logger.error(f"Mentions API error: {media_response.text}")
                return []

            media_data = media_response.json()
            mentions = []

            if 'data' in media_data:
                for media in media_data['data']:
                    if 'comments' in media and 'data' in media['comments']:
                        for comment in media['comments']['data']:
                            text = comment.get('text', '').lower()

                            # Check for @ mentions or questions
                            if '@' in text or '?' in text:
                                item_hash = hash(f"ig_mention:{comment.get('id')}")

                                if item_hash not in self.processed_items:
                                    mentions.append({
                                        'id': comment.get('id'),
                                        'type': 'mention',
                                        'from': comment.get('from', {}).get('username', 'Unknown'),
                                        'message': comment.get('text', ''),
                                        'media_id': media.get('id'),
                                        'timestamp': comment.get('created_time'),
                                        'is_question': '?' in text
                                    })
                                    self.processed_items.add(item_hash)
                                    self.logger.info(f"New Instagram mention from @{comment.get('from', {}).get('username', 'Unknown')}")

            return mentions

        except Exception as e:
            self.logger.error(f"Error getting Instagram mentions: {e}")
            return []

    def _demo_check(self) -> List[Dict]:
        """Generate demo notifications for testing"""
        import random

        if random.random() > 0.3:  # 70% chance of no new items
            return []

        demo_items = [
            {
                'id': f'demo_ig_{int(time.time())}',
                'type': 'comment',
                'from': 'instagram_user',
                'message': '❤️ Love this! Amazing content.',
                'timestamp': datetime.now().isoformat()
            }
        ]

        return demo_items

    def create_action_file(self, item: Dict) -> Path:
        """
        Create action file for Instagram activity

        Args:
            item: Instagram activity data

        Returns:
            Path to created file
        """
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

        if item['type'] == 'comment':
            filename = f'INSTAGRAM_COMMENT_{item.get("id", timestamp)}.md'
        else:
            filename = f'INSTAGRAM_MENTION_{timestamp}.md'

        filepath = self.needs_action / filename

        content = f"""---
type: instagram_{item['type']}
instagram_id: {item.get('id', 'unknown')}
received: {item.get('timestamp', datetime.now().isoformat())}
priority: {'high' if item.get('is_question') else 'medium'}
status: pending
---

# Instagram {'Comment' if item['type'] == 'comment' else 'Mention/Question'}

## {'Comment Details' if item['type'] == 'comment' else 'Mention Details'}
- **From**: @{item.get('from', 'Unknown')}
- **Type**: {item['type']}
- **Time**: {item.get('timestamp', 'Unknown')}

## Message
{item.get('message', 'No message content')}

{f"## Original Post Caption\n{item.get('media_caption', 'N/A')}" if item['type'] == 'comment' else f"## Context\n- **Question**: {'Yes' if item.get('is_question') else 'No'}\n- **Contains @mention**: {'Yes' if '@' in item.get('message', '') else 'No'}"}

## Suggested Actions
- [ ] Read and understand the {'comment' if item['type'] == 'comment' else 'mention'}
- [ ] Consider responding
- [ ] Like the comment if appropriate
- [ ] Create approval request if action needed
- [ ] Mark as processed

## Links
- [View on Instagram](https://www.instagram.com/p/{item.get('media_id', '')})

## Notes
Add any context or notes here before processing.
"""

        filepath.write_text(content, encoding='utf-8')
        self.logger.info(f"Created action file: {filename}")
        return filepath

    def run(self):
        """Main watcher loop"""
        self.logger.info(f"Starting Instagram Watcher (Demo Mode: {self.demo_mode})")
        self.logger.info(f"Checking every {self.check_interval} seconds")

        if not self.demo_mode:
            self.logger.info(f"Monitoring account: {self.ig_account_id}")
            self.logger.info("Using Meta Graph API for monitoring")

        while True:
            try:
                # Check for updates
                updates = self.check_for_updates()

                for update in updates:
                    self.create_action_file(update)
                    self.logger.info(f"New Instagram {update['type']}: {update.get('message', '')[:50]}...")

                if updates:
                    self.logger.info(f"Processed {len(updates)} items")

            except Exception as e:
                self.logger.error(f"Error in watcher loop: {e}")

            time.sleep(self.check_interval)


def main():
    """Main entry point"""
    vault_path = os.getenv('VAULT_PATH', os.getcwd())

    # Create watcher instance
    watcher = InstagramWatcher(vault_path, check_interval=300)  # Check every 5 minutes

    # Run the watcher
    try:
        watcher.run()
    except KeyboardInterrupt:
        watcher.logger.info("Instagram Watcher stopped by user")
    except Exception as e:
        watcher.logger.error(f"Instagram Watcher crashed: {e}")


if __name__ == '__main__':
    main()
