"""
Facebook MCP Server - Post to Facebook using Meta Graph API
Part of Gold Tier AI Employee Implementation
"""

import os
import logging
import requests
from pathlib import Path
from datetime import datetime
from typing import Dict, Optional, List
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class FacebookMCP:
    """
    MCP Server for Facebook operations using Meta Graph API:
    - Post text updates
    - Post photos with captions
    - Post links
    - Get post metrics
    - Manage Facebook Page
    """

    def __init__(self, vault_path: str):
        """
        Initialize Facebook MCP Server

        Args:
            vault_path: Path to the Obsidian vault
        """
        self.vault_path = Path(vault_path)
        self.logger = self._setup_logger()

        # Demo mode flag
        self.demo_mode = os.getenv('FACEBOOK_DEMO_MODE', 'true').lower() == 'true'

        # Facebook credentials
        self.page_id = os.getenv('FACEBOOK_PAGE_ID')
        self.access_token = os.getenv('FACEBOOK_PAGE_ACCESS_TOKEN')

        if not self.demo_mode and not all([self.page_id, self.access_token]):
            self.logger.warning("Facebook API credentials not found. Running in demo mode.")
            self.demo_mode = True

        if not self.demo_mode:
            self.logger.info(f"Facebook MCP initialized for page: {self.page_id}")

    def _setup_logger(self) -> logging.Logger:
        """Setup logging for the MCP server"""
        logger = logging.getLogger('FacebookMCP')
        logger.setLevel(logging.INFO)
        logger.propagate = False  # Prevent duplicate logs to parent handlers

        # Clear any existing handlers
        logger.handlers = []

        # Create logs directory if it doesn't exist
        log_dir = self.vault_path / 'logs'
        log_dir.mkdir(exist_ok=True)

        # File handler
        log_file = log_dir / f'facebook_mcp_{datetime.now().strftime("%Y%m%d")}.log'
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

    def post_text(self, message: str) -> Dict:
        """
        Post a text update to Facebook Page

        Args:
            message: Text message to post

        Returns:
            Dict with post info or error
        """
        if self.demo_mode:
            return self._demo_post(message)

        try:
            url = f"https://graph.facebook.com/v19.0/{self.page_id}/feed"

            params = {
                'message': message,
                'access_token': self.access_token
            }

            response = requests.post(url, data=params)

            if response.status_code != 200:
                return {
                    'success': False,
                    'error': f'Failed to post: {response.text}'
                }

            data = response.json()
            post_id = data.get('id')

            self.logger.info(f"Post published successfully! Post ID: {post_id}")

            return {
                'success': True,
                'post_id': post_id,
                'url': f'https://www.facebook.com/{post_id}',
                'message': message,
                'timestamp': datetime.now().isoformat()
            }

        except Exception as e:
            self.logger.error(f"Error posting to Facebook: {e}")
            return {
                'success': False,
                'error': str(e)
            }

    def post_photo(self, image_url: str, caption: str) -> Dict:
        """
        Post a photo to Facebook Page

        Args:
            image_url: Publicly accessible URL of the image
            caption: Caption for the photo

        Returns:
            Dict with post info or error
        """
        if self.demo_mode:
            return self._demo_post(caption, image_url)

        try:
            url = f"https://graph.facebook.com/v19.0/{self.page_id}/photos"

            params = {
                'url': image_url,
                'caption': caption,
                'access_token': self.access_token
            }

            response = requests.post(url, data=params)

            if response.status_code != 200:
                return {
                    'success': False,
                    'error': f'Failed to post photo: {response.text}'
                }

            data = response.json()
            post_id = data.get('id')

            self.logger.info(f"Photo posted successfully! Post ID: {post_id}")

            return {
                'success': True,
                'post_id': post_id,
                'url': f'https://www.facebook.com/{post_id}',
                'caption': caption,
                'timestamp': datetime.now().isoformat()
            }

        except Exception as e:
            self.logger.error(f"Error posting photo to Facebook: {e}")
            return {
                'success': False,
                'error': str(e)
            }

    def post_link(self, link: str, message: str) -> Dict:
        """
        Post a link to Facebook Page

        Args:
            link: URL to share
            message: Message to accompany the link

        Returns:
            Dict with post info or error
        """
        if self.demo_mode:
            return self._demo_post(message, link)

        try:
            url = f"https://graph.facebook.com/v19.0/{self.page_id}/feed"

            params = {
                'link': link,
                'message': message,
                'access_token': self.access_token
            }

            response = requests.post(url, data=params)

            if response.status_code != 200:
                return {
                    'success': False,
                    'error': f'Failed to post link: {response.text}'
                }

            data = response.json()
            post_id = data.get('id')

            self.logger.info(f"Link posted successfully! Post ID: {post_id}")

            return {
                'success': True,
                'post_id': post_id,
                'url': f'https://www.facebook.com/{post_id}',
                'message': message,
                'link': link,
                'timestamp': datetime.now().isoformat()
            }

        except Exception as e:
            self.logger.error(f"Error posting link to Facebook: {e}")
            return {
                'success': False,
                'error': str(e)
            }

    def _demo_post(self, message: str, media: Optional[str] = None) -> Dict:
        """Demo mode posting"""
        demo_post_id = f"demo_{int(datetime.now().timestamp())}"

        self.logger.info(f"[DEMO] Would post to Facebook:")
        self.logger.info(f"[DEMO] Message: {message[:50]}...")
        if media:
            self.logger.info(f"[DEMO] Media: {media}")

        return {
            'success': True,
            'post_id': demo_post_id,
            'url': f'https://www.facebook.com/{demo_post_id}',
            'message': message,
            'timestamp': datetime.now().isoformat(),
            'demo_mode': True
        }

    def get_post_metrics(self, post_id: str) -> Dict:
        """
        Get metrics for a Facebook post

        Args:
            post_id: Facebook post ID

        Returns:
            Dict with metrics or error
        """
        if self.demo_mode:
            return {
                'success': True,
                'post_id': post_id,
                'metrics': {
                    'likes': 42,
                    'comments': 8,
                    'shares': 5,
                    'reactions': 50
                },
                'demo_mode': True
            }

        try:
            url = f"https://graph.facebook.com/v19.0/{post_id}"

            params = {
                'fields': 'likes.summary(true),comments.summary(true),shares,reactions.summary(true),created_time',
                'access_token': self.access_token
            }

            response = requests.get(url, params=params)

            if response.status_code != 200:
                return {
                    'success': False,
                    'error': f'Failed to get metrics: {response.text}'
                }

            data = response.json()

            return {
                'success': True,
                'post_id': post_id,
                'metrics': {
                    'likes': data.get('likes', {}).get('summary', {}).get('total_count', 0),
                    'comments': data.get('comments', {}).get('summary', {}).get('total_count', 0),
                    'shares': data.get('shares', {}).get('count', 0),
                    'reactions': data.get('reactions', {}).get('summary', {}).get('total_count', 0)
                },
                'created_time': data.get('created_time')
            }

        except Exception as e:
            self.logger.error(f"Error getting metrics: {e}")
            return {
                'success': False,
                'error': str(e)
            }


def main():
    """Test the Facebook MCP server"""
    vault_path = os.getenv('VAULT_PATH', os.getcwd())
    mcp = FacebookMCP(vault_path)

    # Test posting
    result = mcp.post_text("Testing Facebook MCP with Meta Graph API! 🚀 #AI #Automation")
    print(f"Post result: {result}")


if __name__ == '__main__':
    main()
