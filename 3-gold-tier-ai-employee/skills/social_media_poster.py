"""
Social Media Poster - Unified interface for Facebook and Instagram posting
Uses Meta Graph API for reliable, fast posting
Part of Gold Tier AI Employee Implementation
"""

import os
import sys
import logging
from pathlib import Path
from datetime import datetime
from typing import Dict, Optional

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from mcp_servers.facebook_mcp_api import FacebookMCP
from mcp_servers.instagram_mcp_api import InstagramMCP


class SocialMediaPoster:
    """
    Unified social media posting interface
    Handles Facebook and Instagram posting with Meta Graph API
    """

    def __init__(self, vault_path: str = None):
        """
        Initialize Social Media Poster

        Args:
            vault_path: Path to the project vault
        """
        self.vault_path = Path(vault_path) if vault_path else project_root
        self.logger = self._setup_logger()

        # Initialize MCPs
        self.facebook = FacebookMCP(str(self.vault_path))
        self.instagram = InstagramMCP(str(self.vault_path))

        self.logger.info("Social Media Poster initialized")

    def _setup_logger(self) -> logging.Logger:
        """Setup logging"""
        logger = logging.getLogger('SocialMediaPoster')
        logger.setLevel(logging.INFO)

        # Create logs directory
        log_dir = self.vault_path / 'logs'
        log_dir.mkdir(exist_ok=True)

        # File handler
        log_file = log_dir / f'social_media_{datetime.now().strftime("%Y%m%d")}.log'
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

    def post_to_facebook(self, message: str, image_url: Optional[str] = None) -> Dict:
        """
        Post to Facebook Page

        Args:
            message: Text message to post
            image_url: Optional image URL (must be publicly accessible)

        Returns:
            Dict with post result
        """
        self.logger.info("Posting to Facebook...")

        try:
            if image_url:
                result = self.facebook.post_photo(image_url, message)
            else:
                result = self.facebook.post_text(message)

            if result.get('success'):
                self.logger.info(f"✅ Facebook post successful: {result.get('post_id')}")
            else:
                self.logger.error(f"❌ Facebook post failed: {result.get('error')}")

            return result

        except Exception as e:
            self.logger.error(f"Error posting to Facebook: {e}")
            return {
                'success': False,
                'error': str(e)
            }

    def post_to_instagram(self, image_url: str, caption: str) -> Dict:
        """
        Post to Instagram Business Account

        Args:
            image_url: Image URL (must be publicly accessible, direct link)
            caption: Caption for the post

        Returns:
            Dict with post result
        """
        self.logger.info("Posting to Instagram...")

        try:
            result = self.instagram.post_photo(image_url, caption)

            if result.get('success'):
                self.logger.info(f"✅ Instagram post successful: {result.get('media_id')}")
            else:
                self.logger.error(f"❌ Instagram post failed: {result.get('error')}")

            return result

        except Exception as e:
            self.logger.error(f"Error posting to Instagram: {e}")
            return {
                'success': False,
                'error': str(e)
            }

    def post_to_both(self, message: str, image_url: str) -> Dict:
        """
        Post to both Facebook and Instagram

        Args:
            message: Text message/caption
            image_url: Image URL (must be publicly accessible)

        Returns:
            Dict with results from both platforms
        """
        self.logger.info("Posting to both Facebook and Instagram...")

        results = {
            'facebook': self.post_to_facebook(message, image_url),
            'instagram': self.post_to_instagram(image_url, message)
        }

        # Summary
        fb_success = results['facebook'].get('success', False)
        ig_success = results['instagram'].get('success', False)

        if fb_success and ig_success:
            self.logger.info("✅ Posted successfully to both platforms!")
        elif fb_success or ig_success:
            self.logger.warning("⚠️ Posted to one platform only")
        else:
            self.logger.error("❌ Failed to post to both platforms")

        return {
            'success': fb_success or ig_success,
            'facebook': results['facebook'],
            'instagram': results['instagram'],
            'timestamp': datetime.now().isoformat()
        }

    def create_approval_request(self, content: str, image_url: Optional[str] = None,
                               platforms: list = None) -> Dict:
        """
        Create an approval request for social media posting

        Args:
            content: Post content/caption
            image_url: Optional image URL
            platforms: List of platforms ['facebook', 'instagram'] or ['both']

        Returns:
            Dict with approval request info
        """
        if platforms is None:
            platforms = ['both']

        try:
            pending_approval = self.vault_path / 'pending_approval'
            pending_approval.mkdir(exist_ok=True)

            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            approval_file = pending_approval / f'APPROVAL_SOCIAL_POST_{timestamp}.md'

            platforms_str = ', '.join(platforms)

            approval_content = f"""---
type: approval_request
action: social_media_post
platforms: {platforms_str}
created: {datetime.now().isoformat()}
status: pending
---

# Social Media Post Approval Required

## Platforms
{platforms_str}

## Content
{content}

## Media
{f'Image: {image_url}' if image_url else 'Text only'}

## To Approve
1. Review the content above
2. Move this file to `/approved` folder to post
3. The post will be published automatically

## To Reject
Move this file to `/rejected` folder or delete it.

## Metadata
- **Created**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
- **Platforms**: {platforms_str}
- **Has Image**: {'Yes' if image_url else 'No'}

---
*Generated by Social Media Poster*
"""

            approval_file.write_text(approval_content, encoding='utf-8')

            self.logger.info(f"Approval request created: {approval_file}")

            return {
                'success': True,
                'approval_file': str(approval_file),
                'platforms': platforms,
                'timestamp': datetime.now().isoformat()
            }

        except Exception as e:
            self.logger.error(f"Error creating approval request: {e}")
            return {
                'success': False,
                'error': str(e)
            }


def schedule_business_post(topic: str = "Business Update", include_hashtags: bool = True) -> Dict:
    """
    Generate and schedule a business post for approval

    Args:
        topic: Topic for the post
        include_hashtags: Whether to include hashtags

    Returns:
        Dict with post content and status
    """
    # Generate business post content
    hashtags = "#Business #AI #Automation #Productivity" if include_hashtags else ""

    content = f"""🚀 {topic}

We're excited to share our latest progress with AI-powered business automation!

Our AI Employee system is helping businesses:
✅ Automate routine tasks
✅ Improve response times
✅ Increase productivity
✅ Reduce operational costs

Interested in learning more? Let's connect!

{hashtags}
"""

    return {
        'status': 'success',
        'content': content,
        'topic': topic
    }


def main():
    """Test the social media poster"""
    poster = SocialMediaPoster()

    # Test Facebook text post
    print("\n" + "="*60)
    print("Testing Facebook Text Post")
    print("="*60)
    fb_result = poster.post_to_facebook("Testing Social Media Poster with Meta Graph API! 🚀")
    print(f"Result: {fb_result}")

    # Test Instagram post (requires image URL)
    print("\n" + "="*60)
    print("Testing Instagram Post")
    print("="*60)
    test_image = "https://images.unsplash.com/photo-1677442136019-21780ecad995?w=1080&h=1080&fit=crop"
    ig_result = poster.post_to_instagram(test_image, "Testing Social Media Poster! 🚀 #AI #Automation")
    print(f"Result: {ig_result}")


if __name__ == '__main__':
    main()
