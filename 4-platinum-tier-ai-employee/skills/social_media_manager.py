"""
Social Media Manager Skill - Unified social media operations
Part of Gold Tier AI Employee Implementation
"""

import os
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional
import logging

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent))

from mcp_servers.twitter_mcp import TwitterMCP
from mcp_servers.facebook_mcp import FacebookMCP
from mcp_servers.instagram_mcp import InstagramMCP


class SocialMediaManager:
    """
    Unified social media management skill
    - Cross-platform posting
    - Unified analytics
    - Content scheduling
    - Engagement tracking
    """

    def __init__(self, vault_path: str):
        """
        Initialize Social Media Manager

        Args:
            vault_path: Path to the Obsidian vault
        """
        self.vault_path = Path(vault_path)
        self.logger = self._setup_logger()

        # Initialize MCP servers
        self.twitter = TwitterMCP(vault_path)
        self.facebook = FacebookMCP(vault_path)
        self.instagram = InstagramMCP(vault_path)

        # Directories
        self.pending_approval = self.vault_path / 'pending_approval'
        self.approved = self.vault_path / 'approved'
        self.summaries_dir = self.vault_path / 'summaries'

        # Create directories
        self.pending_approval.mkdir(exist_ok=True)
        self.approved.mkdir(exist_ok=True)
        self.summaries_dir.mkdir(exist_ok=True)

    def _setup_logger(self) -> logging.Logger:
        """Setup logging"""
        logger = logging.getLogger('SocialMediaManager')
        logger.setLevel(logging.INFO)

        log_dir = self.vault_path / 'logs'
        log_dir.mkdir(exist_ok=True)

        log_file = log_dir / f'social_media_manager_{datetime.now().strftime("%Y%m%d")}.log'
        fh = logging.FileHandler(log_file)
        fh.setLevel(logging.INFO)

        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)

        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)

        logger.addHandler(fh)
        logger.addHandler(ch)

        return logger

    def post_to_all_platforms(self, content: Dict, require_approval: bool = True) -> Dict:
        """
        Post content to all social media platforms

        Args:
            content: Dict with platform-specific content
                {
                    'twitter': {'text': '...', 'hashtags': [...]},
                    'facebook': {'message': '...', 'link': '...'},
                    'instagram': {'image_url': '...', 'caption': '...'}
                }
            require_approval: Whether to require human approval

        Returns:
            Dict with results for each platform
        """
        if require_approval:
            return self._create_cross_platform_approval(content)

        results = {}

        # Post to Twitter
        if 'twitter' in content:
            twitter_content = content['twitter']
            text = twitter_content.get('text', '')
            hashtags = twitter_content.get('hashtags', [])

            # Add hashtags to text
            if hashtags:
                hashtag_text = ' '.join(f'#{tag.strip("#")}' for tag in hashtags)
                text = f"{text}\n\n{hashtag_text}"

            results['twitter'] = self.twitter.post_tweet(text)

        # Post to Facebook
        if 'facebook' in content:
            facebook_content = content['facebook']
            results['facebook'] = self.facebook.post_to_page(
                message=facebook_content.get('message', ''),
                link=facebook_content.get('link')
            )

        # Post to Instagram
        if 'instagram' in content:
            instagram_content = content['instagram']
            results['instagram'] = self.instagram.post_photo(
                image_url=instagram_content.get('image_url', ''),
                caption=instagram_content.get('caption', '')
            )

        # Log results
        successful = sum(1 for r in results.values() if r.get('success'))
        self.logger.info(f"Posted to {successful}/{len(results)} platforms successfully")

        return {
            'success': successful > 0,
            'platforms': results,
            'total_platforms': len(results),
            'successful_platforms': successful
        }

    def _create_cross_platform_approval(self, content: Dict) -> Dict:
        """Create approval request for cross-platform post"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'SOCIAL_MEDIA_CROSS_PLATFORM_{timestamp}.md'
        filepath = self.pending_approval / filename

        platforms = ', '.join(content.keys())

        approval_content = f"""---
type: social_media_cross_platform
platforms: {platforms}
created: {datetime.now().isoformat()}
status: pending_approval
---

# Cross-Platform Social Media Post

## Platforms
{platforms}

## Content by Platform

"""

        # Add Twitter content
        if 'twitter' in content:
            twitter_content = content['twitter']
            text = twitter_content.get('text', '')
            hashtags = twitter_content.get('hashtags', [])
            approval_content += f"""### Twitter
**Text**: {text}
**Hashtags**: {', '.join(hashtags) if hashtags else 'None'}
**Character Count**: {len(text)}/280

"""

        # Add Facebook content
        if 'facebook' in content:
            facebook_content = content['facebook']
            approval_content += f"""### Facebook
**Message**: {facebook_content.get('message', '')}
**Link**: {facebook_content.get('link', 'None')}

"""

        # Add Instagram content
        if 'instagram' in content:
            instagram_content = content['instagram']
            approval_content += f"""### Instagram
**Caption**: {instagram_content.get('caption', '')}
**Image URL**: {instagram_content.get('image_url', '')}

"""

        approval_content += """## Actions
- [ ] Approve and post to all platforms
- [ ] Edit content
- [ ] Reject

## Instructions
To approve: Move this file to `/approved` folder
To reject: Move this file to `/rejected` folder

---
*Generated by Social Media Manager Skill*
"""

        filepath.write_text(approval_content)
        self.logger.info(f"Created cross-platform approval request: {filename}")

        return {
            'success': True,
            'approval_file': str(filepath),
            'platforms': list(content.keys()),
            'requires_approval': True
        }

    def generate_unified_summary(self, date: Optional[str] = None) -> Dict:
        """
        Generate unified social media summary across all platforms

        Args:
            date: Date to summarize (YYYY-MM-DD), defaults to today

        Returns:
            Dict with summary info
        """
        if date is None:
            date = datetime.now().strftime('%Y-%m-%d')

        self.logger.info(f"Generating unified social media summary for {date}")

        # Collect metrics from all platforms
        twitter_metrics = self._get_twitter_metrics(date)
        facebook_metrics = self._get_facebook_metrics(date)
        instagram_metrics = self._get_instagram_metrics(date)

        # Calculate totals
        total_posts = (twitter_metrics['posts'] + facebook_metrics['posts'] +
                      instagram_metrics['posts'])
        total_engagement = (twitter_metrics['engagement'] + facebook_metrics['engagement'] +
                           instagram_metrics['engagement'])

        # Generate summary content
        summary_content = f"""---
type: social_media_unified_summary
date: {date}
generated: {datetime.now().isoformat()}
---

# Unified Social Media Summary - {date}

## Overview
- **Total Posts**: {total_posts}
- **Total Engagement**: {total_engagement}
- **Platforms Active**: Twitter, Facebook, Instagram

## Platform Breakdown

### Twitter
- **Posts**: {twitter_metrics['posts']}
- **Likes**: {twitter_metrics['likes']}
- **Retweets**: {twitter_metrics['retweets']}
- **Replies**: {twitter_metrics['replies']}
- **Total Engagement**: {twitter_metrics['engagement']}

### Facebook
- **Posts**: {facebook_metrics['posts']}
- **Likes**: {facebook_metrics['likes']}
- **Comments**: {facebook_metrics['comments']}
- **Shares**: {facebook_metrics['shares']}
- **Total Engagement**: {facebook_metrics['engagement']}

### Instagram
- **Posts**: {instagram_metrics['posts']}
- **Likes**: {instagram_metrics['likes']}
- **Comments**: {instagram_metrics['comments']}
- **Saves**: {instagram_metrics['saves']}
- **Total Engagement**: {instagram_metrics['engagement']}

## Top Performing Platform
"""

        # Determine top platform
        platforms = {
            'Twitter': twitter_metrics['engagement'],
            'Facebook': facebook_metrics['engagement'],
            'Instagram': instagram_metrics['engagement']
        }
        top_platform = max(platforms, key=platforms.get)
        summary_content += f"{top_platform} with {platforms[top_platform]} total engagement\n\n"

        summary_content += """## Recommendations
- Continue engaging with your audience across all platforms
- Focus on content types that drive the most engagement
- Maintain consistent posting schedule

---
*Generated by Social Media Manager Skill*
"""

        # Save summary
        summary_file = self.summaries_dir / f'social_media_unified_{date}.md'
        summary_file.write_text(summary_content)

        self.logger.info(f"Unified summary saved: {summary_file}")

        return {
            'success': True,
            'date': date,
            'summary_file': str(summary_file),
            'metrics': {
                'total_posts': total_posts,
                'total_engagement': total_engagement,
                'twitter': twitter_metrics,
                'facebook': facebook_metrics,
                'instagram': instagram_metrics
            }
        }

    def _get_twitter_metrics(self, date: str) -> Dict:
        """Get Twitter metrics for a specific date"""
        # In production, this would query actual data
        # For now, return placeholder data
        return {
            'posts': 0,
            'likes': 0,
            'retweets': 0,
            'replies': 0,
            'engagement': 0
        }

    def _get_facebook_metrics(self, date: str) -> Dict:
        """Get Facebook metrics for a specific date"""
        return {
            'posts': 0,
            'likes': 0,
            'comments': 0,
            'shares': 0,
            'engagement': 0
        }

    def _get_instagram_metrics(self, date: str) -> Dict:
        """Get Instagram metrics for a specific date"""
        return {
            'posts': 0,
            'likes': 0,
            'comments': 0,
            'saves': 0,
            'engagement': 0
        }

    def schedule_cross_platform_post(self, content: Dict, schedule_time: str) -> Dict:
        """
        Schedule a post across multiple platforms

        Args:
            content: Platform-specific content
            schedule_time: When to post (ISO format)

        Returns:
            Dict with schedule info
        """
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'SOCIAL_MEDIA_SCHEDULED_{timestamp}.md'
        filepath = self.vault_path / 'drafts' / filename

        platforms = ', '.join(content.keys())

        schedule_content = f"""---
type: social_media_scheduled
platforms: {platforms}
created: {datetime.now().isoformat()}
scheduled_for: {schedule_time}
status: scheduled
---

# Scheduled Cross-Platform Post

## Schedule
- **Post at**: {schedule_time}
- **Platforms**: {platforms}

## Content
{self._format_content_for_display(content)}

---
*Generated by Social Media Manager Skill*
"""

        filepath.write_text(schedule_content)
        self.logger.info(f"Scheduled cross-platform post for {schedule_time}")

        return {
            'success': True,
            'schedule_file': str(filepath),
            'scheduled_for': schedule_time,
            'platforms': list(content.keys())
        }

    def _format_content_for_display(self, content: Dict) -> str:
        """Format content dict for markdown display"""
        formatted = ""

        for platform, data in content.items():
            formatted += f"\n### {platform.title()}\n"
            for key, value in data.items():
                formatted += f"- **{key.title()}**: {value}\n"

        return formatted


def main():
    """Test the Social Media Manager skill"""
    vault_path = os.getenv('VAULT_PATH', os.getcwd())
    manager = SocialMediaManager(vault_path)

    # Test cross-platform posting
    content = {
        'twitter': {
            'text': 'Excited to announce our new AI Employee system!',
            'hashtags': ['AI', 'Automation', 'Productivity']
        },
        'facebook': {
            'message': 'We are thrilled to introduce our new AI Employee system that revolutionizes workplace automation!',
            'link': 'https://example.com/ai-employee'
        },
        'instagram': {
            'image_url': 'https://example.com/image.jpg',
            'caption': 'Introducing our AI Employee system! 🚀 #AI #Automation #Innovation'
        }
    }

    result = manager.post_to_all_platforms(content, require_approval=True)
    print(f"Cross-platform post result: {result}")

    # Test unified summary
    summary = manager.generate_unified_summary()
    print(f"Unified summary: {summary}")


if __name__ == '__main__':
    main()
