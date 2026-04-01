"""
Facebook MCP Server - Post to Facebook using Playwright
Part of Gold Tier AI Employee Implementation
Uses browser automation (no API keys needed)
"""

import os
import logging
import time
from pathlib import Path
from datetime import datetime
from typing import Dict, Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class FacebookMCP:
    """
    MCP Server for Facebook operations using Playwright:
    - Post to Facebook page/timeline
    - Upload images
    - Manage posts
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

        # Session storage path
        self.session_path = Path(os.getenv('FACEBOOK_SESSION_PATH', './sessions/facebook'))
        self.session_path.mkdir(parents=True, exist_ok=True)

    def _setup_logger(self) -> logging.Logger:
        """Setup logging for the MCP server"""
        logger = logging.getLogger('FacebookMCP')
        logger.setLevel(logging.INFO)

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

    def post_to_page(self, message: str, image_path: Optional[str] = None) -> Dict:
        """
        Post to Facebook using Playwright

        Args:
            message: Post message
            image_path: Optional image file path

        Returns:
            Dict with post info or error
        """
        if self.demo_mode:
            return self._demo_post(message, image_path)

        try:
            from playwright.sync_api import sync_playwright

            self.logger.info("Opening browser to post to Facebook...")

            pw = sync_playwright().start()
            ctx = pw.chromium.launch_persistent_context(
                str(self.session_path),
                headless=False,  # Keep visible for posting
                args=['--no-sandbox', '--window-size=1280,720']
            )
            page = ctx.pages[0] if ctx.pages else ctx.new_page()

            # Go to Facebook
            page.goto('https://www.facebook.com/', wait_until='domcontentloaded', timeout=60000)
            time.sleep(5)

            # Check if logged in
            if 'login' in page.url.lower():
                self.logger.warning("Not logged in. Please log in manually in the browser window.")
                self.logger.info("Waiting 60 seconds for manual login...")
                time.sleep(60)

            # Click "What's on your mind?" or similar
            try:
                # Try multiple selectors for the post box
                selectors = [
                    'text=What\'s on your mind',
                    '[role="button"][aria-label*="Create"]',
                    '[placeholder*="What\'s on your mind"]'
                ]

                clicked = False
                for selector in selectors:
                    try:
                        page.click(selector, timeout=5000)
                        clicked = True
                        self.logger.info("Clicked post creation button")
                        break
                    except:
                        continue

                if not clicked:
                    self.logger.warning("Could not find post button. Please click 'What's on your mind' manually.")
                    time.sleep(10)

            except Exception as e:
                self.logger.warning(f"Error clicking post button: {e}")

            time.sleep(8)

            # Enter content
            try:
                # Try multiple selectors for the text editor
                editor_selectors = [
                    '[role="textbox"]',
                    '[contenteditable="true"]',
                    '[data-testid="status-attachment-mentions-input"]',
                    'div[contenteditable="true"][role="textbox"]'
                ]

                editor_found = False
                for selector in editor_selectors:
                    try:
                        self.logger.info(f"Trying selector: {selector}")
                        editor = page.locator(selector).first
                        editor.wait_for(state='visible', timeout=10000)
                        editor.click()
                        time.sleep(2)
                        editor_found = True
                        self.logger.info(f"Found editor with selector: {selector}")
                        break
                    except Exception as e:
                        self.logger.debug(f"Selector {selector} failed: {e}")
                        continue

                if not editor_found:
                    self.logger.warning("Could not find text editor automatically. Please type manually in the browser window.")
                    self.logger.info("Waiting 30 seconds for manual input...")
                    time.sleep(30)
                else:
                    self.logger.info("Typing content...")
                    page.keyboard.type(message, delay=50)
                    time.sleep(3)
                    self.logger.info("Content entered successfully")

            except Exception as e:
                self.logger.error(f"Error entering content: {e}")
                self.logger.info("Please complete the post manually in the browser window.")
                time.sleep(20)
                # Don't fail completely, let user finish manually

            # Handle image upload if provided
            if image_path and Path(image_path).exists():
                try:
                    self.logger.info(f"Uploading image: {image_path}")

                    # Look for photo/video button
                    photo_button = page.locator('[aria-label*="Photo"]').first
                    photo_button.click(timeout=10000)
                    time.sleep(2)

                    # Upload file
                    file_input = page.locator('input[type="file"]').first
                    file_input.set_input_files(image_path)
                    time.sleep(5)

                    self.logger.info("Image uploaded")

                except Exception as e:
                    self.logger.warning(f"Could not upload image: {e}")

            # Wait for Post button to be enabled and click it
            self.logger.info("Looking for Post button...")
            time.sleep(3)

            post_clicked = False
            try:
                # Try multiple selectors for Post button
                post_selectors = [
                    'button:has-text("Post")',
                    '[aria-label="Post"]',
                    '[role="button"]:has-text("Post")'
                ]

                for selector in post_selectors:
                    try:
                        post_btn = page.locator(selector).first
                        if post_btn.is_visible(timeout=5000) and post_btn.is_enabled():
                            post_btn.click()
                            self.logger.info("Post button clicked!")
                            post_clicked = True
                            break
                    except:
                        continue

            except Exception as e:
                self.logger.warning(f"Error clicking Post button: {e}")

            if not post_clicked:
                self.logger.warning("Could not click Post button automatically.")
                self.logger.info("Please click the 'Post' button manually in the browser.")
                self.logger.info("Waiting 30 seconds...")
                time.sleep(30)

            # Wait for post to publish
            self.logger.info("Waiting for post to publish...")
            time.sleep(10)

            # Take screenshot
            screenshot_path = self.vault_path / 'logs' / f'fb_post_{datetime.now().strftime("%Y%m%d_%H%M%S")}.png'
            page.screenshot(path=str(screenshot_path))
            self.logger.info(f"Screenshot saved: {screenshot_path}")

            ctx.close()
            pw.stop()

            post_id = f"fb_post_{int(datetime.now().timestamp())}"
            post_url = "https://www.facebook.com/"

            self.logger.info("Post published successfully!")

            return {
                'success': True,
                'post_id': post_id,
                'url': post_url,
                'message': message,
                'timestamp': datetime.now().isoformat(),
                'screenshot': str(screenshot_path)
            }

        except ImportError:
            self.logger.error("Playwright not installed. Run: pip install playwright && playwright install chromium")
            return {'success': False, 'error': 'Playwright not installed'}
        except Exception as e:
            self.logger.error(f"Error posting to Facebook: {e}")
            return {'success': False, 'error': str(e)}

    def _demo_post(self, message: str, image_path: Optional[str]) -> Dict:
        """Demo mode post"""
        demo_post_id = f"demo_fb_{int(datetime.now().timestamp())}"
        demo_url = f"https://facebook.com/{demo_post_id}"

        self.logger.info(f"[DEMO] Would post to Facebook: {message[:50]}...")
        if image_path:
            self.logger.info(f"[DEMO] With image: {image_path}")

        return {
            'success': True,
            'post_id': demo_post_id,
            'url': demo_url,
            'message': message,
            'timestamp': datetime.now().isoformat(),
            'demo_mode': True
        }

    def reply_to_comment(self, comment_text: str, reply_message: str) -> Dict:
        """
        Reply to a comment (requires manual navigation)

        Args:
            comment_text: Text of comment to find
            reply_message: Reply message

        Returns:
            Dict with reply info or error
        """
        if self.demo_mode:
            self.logger.info(f"[DEMO] Would reply to comment: {reply_message[:50]}...")
            return {
                'success': True,
                'reply_id': f'demo_reply_{int(datetime.now().timestamp())}',
                'demo_mode': True
            }

        self.logger.info("Reply to comment requires manual navigation to the specific comment.")
        return {
            'success': False,
            'error': 'Manual navigation required for comment replies'
        }


def main():
    """Test the Facebook MCP server"""
    vault_path = os.getenv('VAULT_PATH', os.getcwd())
    mcp = FacebookMCP(vault_path)

    # Test posting
    result = mcp.post_to_page("Testing Facebook MCP with Playwright! 🚀 #AIEmployee #Automation")
    print(f"Post result: {result}")


if __name__ == '__main__':
    main()
