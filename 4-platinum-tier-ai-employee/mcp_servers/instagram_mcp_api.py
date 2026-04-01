"""
Instagram MCP Server - Post to Instagram using Meta Graph API
Part of Gold Tier AI Employee Implementation
"""

import os
import logging
import requests
import time
from pathlib import Path
from datetime import datetime
from typing import Dict, Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class InstagramMCP:
    """
    MCP Server for Instagram operations using Meta Graph API:
    - Post photos with captions
    - Post carousel (multiple images)
    - Get post metrics
    - Manage Instagram Business account
    """

    def __init__(self, vault_path: str):
        """
        Initialize Instagram MCP Server

        Args:
            vault_path: Path to the Obsidian vault
        """
        self.vault_path = Path(vault_path)
        self.logger = self._setup_logger()

        # Demo mode flag
        self.demo_mode = os.getenv('INSTAGRAM_DEMO_MODE', 'true').lower() == 'true'

        # Instagram credentials
        self.ig_account_id = os.getenv('INSTAGRAM_BUSINESS_ACCOUNT_ID')
        self.access_token = os.getenv('INSTAGRAM_ACCESS_TOKEN')

        if not self.demo_mode and not all([self.ig_account_id, self.access_token]):
            self.logger.warning("Instagram API credentials not found. Running in demo mode.")
            self.demo_mode = True

        if not self.demo_mode:
            self.logger.info(f"Instagram MCP initialized for account: {self.ig_account_id}")

    def _setup_logger(self) -> logging.Logger:
        """Setup logging for the MCP server"""
        logger = logging.getLogger('InstagramMCP')
        logger.setLevel(logging.INFO)
        logger.propagate = False  # Prevent duplicate logs to parent handlers

        # Clear any existing handlers
        logger.handlers = []

        # Create logs directory if it doesn't exist
        log_dir = self.vault_path / 'logs'
        log_dir.mkdir(exist_ok=True)

        # File handler
        log_file = log_dir / f'instagram_mcp_{datetime.now().strftime("%Y%m%d")}.log'
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

    def post_photo(self, image_path: str, caption: str) -> Dict:
        """
        Post a photo to Instagram using Meta Graph API

        Args:
            image_path: Path to the image file (must be publicly accessible URL or local file)
            caption: Caption for the post

        Returns:
            Dict with post info or error
        """
        if self.demo_mode:
            return self._demo_post_photo(image_path, caption)

        try:
            # Step 1: Upload image and get URL (if local file)
            image_url = self._get_image_url(image_path)

            # Step 2: Create media container
            self.logger.info(f"Creating media container for: {image_path}")
            container_url = f"https://graph.facebook.com/v19.0/{self.ig_account_id}/media"

            container_params = {
                'image_url': image_url,
                'caption': caption,
                'access_token': self.access_token
            }

            container_response = requests.post(container_url, data=container_params)

            if container_response.status_code != 200:
                return {
                    'success': False,
                    'error': f'Failed to create container: {container_response.text}'
                }

            container_data = container_response.json()
            creation_id = container_data.get('id')

            self.logger.info(f"Media container created: {creation_id}")

            # Step 3: Publish the media
            time.sleep(2)  # Wait a bit for Instagram to process the image

            publish_url = f"https://graph.facebook.com/v19.0/{self.ig_account_id}/media_publish"

            publish_params = {
                'creation_id': creation_id,
                'access_token': self.access_token
            }

            publish_response = requests.post(publish_url, data=publish_params)

            if publish_response.status_code != 200:
                return {
                    'success': False,
                    'error': f'Failed to publish: {publish_response.text}'
                }

            publish_data = publish_response.json()
            media_id = publish_data.get('id')

            self.logger.info(f"Post published successfully! Media ID: {media_id}")

            return {
                'success': True,
                'media_id': media_id,
                'url': f'https://www.instagram.com/p/{media_id}/',
                'caption': caption,
                'timestamp': datetime.now().isoformat()
            }

        except Exception as e:
            self.logger.error(f"Error posting to Instagram: {e}")
            return {
                'success': False,
                'error': str(e)
            }

    def _get_image_url(self, image_path: str) -> str:
        """
        Get publicly accessible URL for image

        Args:
            image_path: Local file path or URL

        Returns:
            Publicly accessible URL
        """
        # If already a URL, return it
        if image_path.startswith('http://') or image_path.startswith('https://'):
            return image_path

        # For local files, you need to upload to a public server
        # For now, we'll assume you have a way to host images
        # You could use services like Imgur, Cloudinary, or your own server

        self.logger.warning("Local file detected. You need to upload it to a public URL first.")
        self.logger.warning("For testing, use a publicly accessible image URL.")

        raise ValueError("Image must be a publicly accessible URL. Upload your image to a hosting service first.")

    def _demo_post_photo(self, image_path: str, caption: str) -> Dict:
        """Demo mode photo posting"""
        demo_media_id = f"demo_{int(datetime.now().timestamp())}"

        self.logger.info(f"[DEMO] Would post to Instagram:")
        self.logger.info(f"[DEMO] Image: {image_path}")
        self.logger.info(f"[DEMO] Caption: {caption[:50]}...")

        return {
            'success': True,
            'media_id': demo_media_id,
            'url': f'https://www.instagram.com/p/{demo_media_id}/',
            'caption': caption,
            'timestamp': datetime.now().isoformat(),
            'demo_mode': True
        }

    def get_post_metrics(self, media_id: str) -> Dict:
        """
        Get metrics for an Instagram post

        Args:
            media_id: Instagram media ID

        Returns:
            Dict with metrics or error
        """
        if self.demo_mode:
            return {
                'success': True,
                'media_id': media_id,
                'metrics': {
                    'likes': 42,
                    'comments': 8,
                    'shares': 5,
                    'reach': 1250,
                    'impressions': 1500
                },
                'demo_mode': True
            }

        try:
            url = f"https://graph.facebook.com/v19.0/{media_id}"

            params = {
                'fields': 'like_count,comments_count,timestamp,media_url,permalink',
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
                'media_id': media_id,
                'metrics': {
                    'likes': data.get('like_count', 0),
                    'comments': data.get('comments_count', 0),
                },
                'timestamp': data.get('timestamp'),
                'permalink': data.get('permalink')
            }

        except Exception as e:
            self.logger.error(f"Error getting metrics: {e}")
            return {
                'success': False,
                'error': str(e)
            }


def main():
    """Test the Instagram MCP server"""
    vault_path = os.getenv('VAULT_PATH', os.getcwd())
    mcp = InstagramMCP(vault_path)

    # Test posting (use a publicly accessible image URL)
    test_image = "https://picsum.photos/1080/1080"  # Random test image
    test_caption = "Testing Instagram MCP with Meta Graph API! 🚀 #AI #Automation"

    result = mcp.post_photo(test_image, test_caption)
    print(f"Post result: {result}")


if __name__ == '__main__':
    main()
