"""
Facebook Watcher - Monitor Facebook using Meta Graph API
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


class FacebookWatcher:
    """
    Monitors Facebook using Meta Graph API:
    - Page comments
    - Page posts engagement
    - Notifications via page insights
    """

    def __init__(self, vault_path: str, check_interval: int = 300):
        """
        Initialize Facebook Watcher

        Args:
            vault_path: Path to the Obsidian vault
            check_interval: Seconds between checks (default 5 minutes)
        """
        self.vault_path = Path(vault_path)
        self.needs_action = self.vault_path / 'needs_action'
        self.check_interval = check_interval
        self.logger = self._setup_logger()

        # Meta API credentials
        self.page_id = os.getenv('FACEBOOK_PAGE_ID')
        self.access_token = os.getenv('FACEBOOK_PAGE_ACCESS_TOKEN')

        # Demo mode flag
        self.demo_mode = os.getenv('FACEBOOK_DEMO_MODE', 'true').lower() == 'true'

        # Validate credentials
        if not self.demo_mode and not all([self.page_id, self.access_token]):
            self.logger.warning("Facebook API credentials not found. Running in demo mode.")
            self.demo_mode = True

        # Track processed items
        self.processed_items = set()
        self.last_check_time = datetime.now() - timedelta(minutes=5)

        # Create required directories
        self.needs_action.mkdir(exist_ok=True)

        if not self.demo_mode:
            self.logger.info(f"Facebook Watcher initialized for page: {self.page_id}")
        else:
            self.logger.info("Facebook Watcher initialized in DEMO mode")

    def _setup_logger(self) -> logging.Logger:
        """Setup logging for the watcher"""
        logger = logging.getLogger('FacebookWatcher')
        logger.setLevel(logging.INFO)

        # Create logs directory if it doesn't exist
        log_dir = self.vault_path / 'logs'
        log_dir.mkdir(exist_ok=True)

        # File handler
        log_file = log_dir / f'facebook_watcher_{datetime.now().strftime("%Y%m%d")}.log'
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
        """Check for new Facebook activity using Meta Graph API"""
        if self.demo_mode:
            return self._demo_check()

        try:
            updates = []

            # Check for new comments on recent posts
            comments = self._get_recent_comments()
            updates.extend(comments)

            # Check for new post engagements
            engagements = self._get_post_engagements()
            updates.extend(engagements)

            self.last_check_time = datetime.now()

            return updates

        except Exception as e:
            self.logger.error(f"Error checking Facebook: {e}")
            return []

    def _get_recent_comments(self) -> List[Dict]:
        """Get recent comments on page posts"""
        try:
            # Get comments on page posts
            url = f"https://graph.facebook.com/v19.0/{self.page_id}/feed"
            params = {
                'fields': 'comments.fields(from,message,created_time,can_remove)',
                'limit': 5,
                'access_token': self.access_token
            }

            response = requests.get(url, params=params, timeout=30)

            if response.status_code != 200:
                self.logger.error(f"API error: {response.text}")
                return []

            data = response.json()
            comments = []

            if 'data' in data:
                for post in data['data']:
                    if 'comments' in post and 'data' in post['comments']:
                        for comment in post['comments']['data']:
                            comment_time = datetime.strptime(
                                comment.get('created_time', ''),
                                '%Y-%m-%dT%H:%M:%S%z'
                            ) if comment.get('created_time') else None

                            # Only get comments since last check
                            if comment_time and comment_time > self.last_check_time:
                                item_hash = hash(f"comment:{comment.get('id')}")

                                if item_hash not in self.processed_items:
                                    comments.append({
                                        'id': comment.get('id'),
                                        'type': 'comment',
                                        'from': comment.get('from', {}).get('name', 'Unknown'),
                                        'message': comment.get('message', ''),
                                        'post_id': post.get('id'),
                                        'timestamp': comment.get('created_time'),
                                        'can_remove': comment.get('can_remove', False)
                                    })
                                    self.processed_items.add(item_hash)
                                    self.logger.info(f"New comment from {comment.get('from', {}).get('name', 'Unknown')}")

            return comments

        except Exception as e:
            self.logger.error(f"Error getting comments: {e}")
            return []

    def _get_post_engagements(self) -> List[Dict]:
        """Get recent post engagements (likes, shares)"""
        try:
            url = f"https://graph.facebook.com/v19.0/{self.page_id}/feed"
            params = {
                'fields': 'message,created_time,likes.summary(true),shares.summary(true)',
                'limit': 3,
                'access_token': self.access_token
            }

            response = requests.get(url, params=params, timeout=30)

            if response.status_code != 200:
                self.logger.error(f"API error: {response.text}")
                return []

            data = response.json()
            engagements = []

            if 'data' in data:
                for post in data['data']:
                    likes_count = post.get('likes', {}).get('summary', {}).get('total_count', 0)
                    shares_count = post.get('shares', {}).get('count', 0)

                    # Flag high engagement posts
                    if likes_count > 50 or shares_count > 10:
                        item_hash = hash(f"engagement:{post.get('id')}")

                        if item_hash not in self.processed_items:
                            engagements.append({
                                'id': post.get('id'),
                                'type': 'high_engagement',
                                'message': post.get('message', '')[:100],
                                'likes': likes_count,
                                'shares': shares_count,
                                'timestamp': post.get('created_time')
                            })
                            self.processed_items.add(item_hash)
                            self.logger.info(f"High engagement post: {likes_count} likes, {shares_count} shares")

            return engagements

        except Exception as e:
            self.logger.error(f"Error getting engagements: {e}")
            return []

    def _demo_check(self) -> List[Dict]:
        """Generate demo notifications for testing"""
        import random

        if random.random() > 0.3:  # 70% chance of no new items
            return []

        demo_items = [
            {
                'id': f'demo_fb_{int(time.time())}',
                'type': 'comment',
                'from': 'John Doe',
                'message': 'Great content! Very helpful information.',
                'timestamp': datetime.now().isoformat()
            }
        ]

        return demo_items

    def create_action_file(self, item: Dict) -> Path:
        """
        Create action file for Facebook activity

        Args:
            item: Facebook activity data

        Returns:
            Path to created file
        """
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

        if item['type'] == 'comment':
            filename = f'FACEBOOK_COMMENT_{item.get("id", timestamp)}.md'
        else:
            filename = f'FACEBOOK_ENGAGEMENT_{timestamp}.md'

        filepath = self.needs_action / filename

        content = f"""---
type: facebook_{item['type']}
facebook_id: {item.get('id', 'unknown')}
received: {item.get('timestamp', datetime.now().isoformat())}
priority: {'high' if item['type'] == 'comment' else 'medium'}
status: pending
---

# Facebook {'Comment' if item['type'] == 'comment' else 'High Engagement'}

## {'Comment Details' if item['type'] == 'comment' else 'Engagement Details'}
- **From**: {item.get('from', 'N/A' if item['type'] == 'comment' else 'Page Analytics')}
- **Type**: {item['type']}
- **Time**: {item.get('timestamp', 'Unknown')}

## {'Message' if item['type'] == 'comment' else 'Post Content'}
{item.get('message', 'No message content')}

{f"## Post ID\n{item.get('post_id', 'N/A')}" if item['type'] == 'comment' else f"## Metrics\n- **Likes**: {item.get('likes', 0)}\n- **Shares**: {item.get('shares', 0)}"}

## Suggested Actions
{'- [ ] Read and understand the comment' if item['type'] == 'comment' else '- [ ] Review high-performing post'}
- [ ] Consider responding/engaging
- [ ] Create approval request if action needed
- [ ] Mark as processed

## Links
- [View on Facebook](https://www.facebook.com/{item.get('post_id' if item['type'] == 'comment' else item.get('id', ''))})

## Notes
Add any context or notes here before processing.
"""

        filepath.write_text(content, encoding='utf-8')
        self.logger.info(f"Created action file: {filename}")
        return filepath

    def run(self):
        """Main watcher loop"""
        self.logger.info(f"Starting Facebook Watcher (Demo Mode: {self.demo_mode})")
        self.logger.info(f"Checking every {self.check_interval} seconds")

        if not self.demo_mode:
            self.logger.info(f"Monitoring page: {self.page_id}")
            self.logger.info("Using Meta Graph API for monitoring")

        while True:
            try:
                # Check for updates
                updates = self.check_for_updates()

                for update in updates:
                    self.create_action_file(update)
                    self.logger.info(f"New Facebook {update['type']}: {update.get('message', '')[:50]}...")

                if updates:
                    self.logger.info(f"Processed {len(updates)} items")

            except Exception as e:
                self.logger.error(f"Error in watcher loop: {e}")

            time.sleep(self.check_interval)


def main():
    """Main entry point"""
    vault_path = os.getenv('VAULT_PATH', os.getcwd())

    # Create watcher instance
    watcher = FacebookWatcher(vault_path, check_interval=300)  # Check every 5 minutes

    # Run the watcher
    try:
        watcher.run()
    except KeyboardInterrupt:
        watcher.logger.info("Facebook Watcher stopped by user")
    except Exception as e:
        watcher.logger.error(f"Facebook Watcher crashed: {e}")


if __name__ == '__main__':
    main()
