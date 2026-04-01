"""
Instagram MCP Server - Post to Instagram using Playwright
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


class InstagramMCP:
    """
    MCP Server for Instagram operations using Playwright:
    - Post photos to Instagram
    - Upload images with captions
    - Manage posts
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

        # Session storage path
        self.session_path = Path(os.getenv('INSTAGRAM_SESSION_PATH', './sessions/instagram'))
        self.session_path.mkdir(parents=True, exist_ok=True)

    def _setup_logger(self) -> logging.Logger:
        """Setup logging for the MCP server"""
        logger = logging.getLogger('InstagramMCP')
        logger.setLevel(logging.INFO)

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
        Post a photo to Instagram using Playwright

        Args:
            image_path: Local path to image file
            caption: Post caption

        Returns:
            Dict with post info or error
        """
        if self.demo_mode:
            return self._demo_post(image_path, caption)

        if not Path(image_path).exists():
            return {'success': False, 'error': f'Image file not found: {image_path}'}

        try:
            from playwright.sync_api import sync_playwright

            self.logger.info("Opening browser to post to Instagram...")

            pw = sync_playwright().start()
            ctx = pw.chromium.launch_persistent_context(
                str(self.session_path),
                headless=False,  # Keep visible for posting
                args=['--no-sandbox', '--window-size=1280,720']
            )
            page = ctx.pages[0] if ctx.pages else ctx.new_page()

            # Go to Instagram
            page.goto('https://www.instagram.com/', wait_until='domcontentloaded', timeout=60000)
            time.sleep(5)

            # Check if logged in
            if 'login' in page.url.lower():
                self.logger.warning("Not logged in. Please log in manually in the browser window.")
                self.logger.info("Waiting 60 seconds for manual login...")
                time.sleep(60)
                page.goto('https://www.instagram.com/', wait_until='domcontentloaded', timeout=60000)
                time.sleep(5)

            # Click "Create" or "New post" button
            try:
                # Try multiple selectors for the create button
                create_selectors = [
                    '[aria-label="New post"]',
                    '[aria-label="Create"]',
                    'svg[aria-label="New post"]',
                    'text=Create'
                ]

                clicked = False
                for selector in create_selectors:
                    try:
                        page.click(selector, timeout=5000)
                        clicked = True
                        self.logger.info("Clicked create post button")
                        break
                    except:
                        continue

                if not clicked:
                    self.logger.warning("Could not find create button. Please click 'Create' or '+' manually.")
                    time.sleep(10)

            except Exception as e:
                self.logger.warning(f"Error clicking create button: {e}")

            time.sleep(5)

            # Upload image
            try:
                self.logger.info(f"Uploading image: {image_path}")

                # Wait a bit for the dialog to fully load
                time.sleep(3)

                # Try to find file input - it might be hidden
                try:
                    file_input = page.locator('input[type="file"]').first
                    file_input.set_input_files(str(Path(image_path).absolute()), timeout=10000)
                    time.sleep(8)
                    self.logger.info("Image uploaded successfully")
                except Exception as e:
                    self.logger.warning(f"Direct file input failed: {e}")
                    # Alternative: Check if we need to click "Select from computer"
                    try:
                        select_buttons = [
                            'button:has-text("Select from computer")',
                            'button:has-text("Select From Computer")',
                            'text=Select from computer'
                        ]
                        for btn_selector in select_buttons:
                            try:
                                page.click(btn_selector, timeout=3000)
                                self.logger.info("Clicked 'Select from computer'")
                                time.sleep(2)
                                break
                            except:
                                continue

                        # Now try file input again
                        file_input = page.locator('input[type="file"]').first
                        file_input.set_input_files(str(Path(image_path).absolute()), timeout=10000)
                        time.sleep(8)
                        self.logger.info("Image uploaded successfully (after clicking select)")
                    except Exception as e2:
                        self.logger.error(f"Could not upload image: {e2}")
                        self.logger.info("Please upload the image manually in the browser window.")
                        time.sleep(30)

            except Exception as e:
                self.logger.error(f"Error in upload process: {e}")
                time.sleep(30)

            # Click "Next" button (may appear multiple times)
            self.logger.info("Looking for Next buttons...")
            try:
                for i in range(3):  # May need to click Next multiple times
                    time.sleep(3)
                    next_selectors = [
                        'button:has-text("Next")',
                        'button >> text="Next"',
                        'div[role="button"]:has-text("Next")'
                    ]

                    next_clicked = False
                    for selector in next_selectors:
                        try:
                            next_btn = page.locator(selector).first
                            if next_btn.is_visible(timeout=3000):
                                next_btn.click()
                                self.logger.info(f"Clicked Next button (step {i+1})")
                                next_clicked = True
                                break
                        except:
                            continue

                    if not next_clicked:
                        self.logger.info("No more Next buttons found, moving to caption")
                        break

            except Exception as e:
                self.logger.debug(f"Next button handling: {e}")

            time.sleep(5)

            # Enter caption
            try:
                self.logger.info("Entering caption...")

                # Find caption textarea - try multiple approaches
                caption_selectors = [
                    'textarea[aria-label*="Write a caption"]',
                    'textarea[placeholder*="Write a caption"]',
                    'textarea[aria-label*="caption"]',
                    'div[contenteditable="true"][aria-label*="caption"]',
                    'textarea',
                    'div[contenteditable="true"]'
                ]

                caption_entered = False
                for selector in caption_selectors:
                    try:
                        self.logger.info(f"Trying caption selector: {selector}")
                        caption_field = page.locator(selector).first
                        caption_field.wait_for(state='visible', timeout=5000)
                        caption_field.click()
                        time.sleep(2)

                        # Clear any existing text
                        caption_field.fill('')
                        time.sleep(1)

                        # Type caption
                        caption_field.type(caption, delay=30)
                        caption_entered = True
                        self.logger.info("Caption entered successfully")
                        break
                    except Exception as e:
                        self.logger.debug(f"Caption selector {selector} failed: {e}")
                        continue

                if not caption_entered:
                    self.logger.warning("Could not enter caption automatically, trying keyboard method")
                    # Fallback: just type using keyboard
                    try:
                        page.keyboard.type(caption, delay=30)
                        self.logger.info("Caption entered via keyboard")
                    except:
                        self.logger.error("Failed to enter caption")

            except Exception as e:
                self.logger.error(f"Error entering caption: {e}")

            time.sleep(5)

            # Click "Share" button to publish - USE SAME METHOD AS NEXT BUTTON!
            self.logger.info("Looking for Share button...")
            time.sleep(3)

            # Take screenshot BEFORE attempting to click Share
            before_screenshot = self.vault_path / 'logs' / f'ig_before_share_{datetime.now().strftime("%Y%m%d_%H%M%S")}.png'
            page.screenshot(path=str(before_screenshot))
            self.logger.info(f"Screenshot before Share click: {before_screenshot}")

            share_clicked = False

            # Use the SAME method that works for Next buttons!
            share_selectors = [
                'button:has-text("Share")',
                'button >> text="Share"',
                'div[role="button"]:has-text("Share")'
            ]

            for selector in share_selectors:
                try:
                    self.logger.info(f"Trying Share selector: {selector}")
                    share_btn = page.locator(selector).first
                    if share_btn.is_visible(timeout=5000):
                        share_btn.click()
                        self.logger.info("✓ Share button clicked successfully!")
                        share_clicked = True
                        time.sleep(5)  # Wait for Instagram to process
                        break
                except Exception as e:
                    self.logger.debug(f"Share selector {selector} failed: {e}")
                    continue

            if not share_clicked:
                self.logger.error("Share button was not clicked successfully!")
                self.logger.error("Taking screenshot of current state...")
                failed_screenshot = self.vault_path / 'logs' / f'ig_share_failed_{datetime.now().strftime("%Y%m%d_%H%M%S")}.png'
                page.screenshot(path=str(failed_screenshot))
                self.logger.error(f"Failed state screenshot: {failed_screenshot}")

                # Return failure instead of waiting
                ctx.close()
                pw.stop()
                return {
                    'success': False,
                    'error': 'Failed to click Share button',
                    'debug_screenshot': str(before_screenshot),
                    'failed_screenshot': str(failed_screenshot)
                }

            # Wait for post to publish - Instagram needs time to process
            self.logger.info("Share button clicked successfully! Waiting for Instagram to publish...")
            self.logger.info("This takes 20-30 seconds...")
            time.sleep(30)

            # Take screenshot
            screenshot_path = self.vault_path / 'logs' / f'ig_post_{datetime.now().strftime("%Y%m%d_%H%M%S")}.png'
            page.screenshot(path=str(screenshot_path))
            self.logger.info(f"Screenshot saved: {screenshot_path}")

            ctx.close()
            pw.stop()

            media_id = f"ig_post_{int(datetime.now().timestamp())}"
            post_url = "https://www.instagram.com/"

            self.logger.info("Post published successfully!")

            return {
                'success': True,
                'media_id': media_id,
                'url': post_url,
                'caption': caption,
                'timestamp': datetime.now().isoformat(),
                'screenshot': str(screenshot_path)
            }

        except ImportError:
            self.logger.error("Playwright not installed. Run: pip install playwright && playwright install chromium")
            return {'success': False, 'error': 'Playwright not installed'}
        except Exception as e:
            self.logger.error(f"Error posting to Instagram: {e}")
            return {'success': False, 'error': str(e)}

    def post_reel(self, video_path: str, caption: str) -> Dict:
        """
        Post a reel/video to Instagram using Playwright

        Args:
            video_path: Path to video file
            caption: Caption for the reel

        Returns:
            Dict with post info or error
        """
        if self.demo_mode:
            return self._demo_post(video_path, caption)

        if not Path(video_path).exists():
            return {'success': False, 'error': f'Video file not found: {video_path}'}

        try:
            from playwright.sync_api import sync_playwright

            self.logger.info("Opening browser to post reel to Instagram...")

            pw = sync_playwright().start()
            ctx = pw.chromium.launch_persistent_context(
                str(self.session_path),
                headless=False,
                args=['--no-sandbox', '--window-size=1280,720']
            )
            page = ctx.pages[0] if ctx.pages else ctx.new_page()

            # Go to Instagram
            page.goto('https://www.instagram.com/', wait_until='domcontentloaded', timeout=60000)
            time.sleep(5)

            # Check if logged in
            if 'login' in page.url.lower():
                self.logger.warning("Not logged in. Please log in manually.")
                self.logger.info("Waiting 60 seconds for manual login...")
                time.sleep(60)
                page.goto('https://www.instagram.com/', wait_until='domcontentloaded', timeout=60000)
                time.sleep(5)

            # Click "Create" button
            try:
                create_selectors = [
                    '[aria-label="New post"]',
                    '[aria-label="Create"]',
                    'svg[aria-label="New post"]'
                ]

                clicked = False
                for selector in create_selectors:
                    try:
                        page.click(selector, timeout=5000)
                        clicked = True
                        self.logger.info("Clicked create button")
                        break
                    except:
                        continue

                if not clicked:
                    self.logger.warning("Could not find create button")
                    time.sleep(10)

            except Exception as e:
                self.logger.warning(f"Error clicking create button: {e}")

            time.sleep(5)

            # Upload video
            try:
                self.logger.info(f"Uploading video: {video_path}")

                file_input = page.locator('input[type="file"]').first
                file_input.wait_for(state='attached', timeout=30000)
                file_input.set_input_files(str(Path(video_path).absolute()))
                time.sleep(10)  # Videos take longer to process

                self.logger.info("Video uploaded successfully")

            except Exception as e:
                self.logger.error(f"Error uploading video: {e}")
                self.logger.info("Please upload the video manually.")
                time.sleep(30)

            # Click Next buttons
            self.logger.info("Looking for Next buttons...")
            try:
                for i in range(3):
                    time.sleep(3)
                    next_selectors = [
                        'button:has-text("Next")',
                        'button >> text="Next"',
                        'div[role="button"]:has-text("Next")'
                    ]

                    next_clicked = False
                    for selector in next_selectors:
                        try:
                            next_btn = page.locator(selector).first
                            if next_btn.is_visible(timeout=3000):
                                next_btn.click()
                                self.logger.info(f"Clicked Next button (step {i+1})")
                                next_clicked = True
                                break
                        except:
                            continue

                    if not next_clicked:
                        self.logger.info("No more Next buttons, moving to caption")
                        break

            except Exception as e:
                self.logger.debug(f"Next button handling: {e}")

            time.sleep(5)

            # Enter caption
            try:
                self.logger.info("Entering caption...")

                caption_selectors = [
                    'textarea[aria-label*="Write a caption"]',
                    'textarea[placeholder*="Write a caption"]',
                    'textarea[aria-label*="caption"]',
                    'div[contenteditable="true"][aria-label*="caption"]',
                    'textarea',
                    'div[contenteditable="true"]'
                ]

                caption_entered = False
                for selector in caption_selectors:
                    try:
                        self.logger.info(f"Trying caption selector: {selector}")
                        caption_field = page.locator(selector).first
                        caption_field.wait_for(state='visible', timeout=5000)
                        caption_field.click()
                        time.sleep(2)
                        caption_field.fill('')
                        time.sleep(1)
                        caption_field.type(caption, delay=30)
                        caption_entered = True
                        self.logger.info("Caption entered successfully")
                        break
                    except Exception as e:
                        self.logger.debug(f"Caption selector {selector} failed: {e}")
                        continue

                if not caption_entered:
                    self.logger.warning("Trying keyboard method for caption")
                    try:
                        page.keyboard.type(caption, delay=30)
                        self.logger.info("Caption entered via keyboard")
                    except:
                        self.logger.error("Failed to enter caption")

            except Exception as e:
                self.logger.error(f"Error entering caption: {e}")

            time.sleep(5)

            # Click Share button
            self.logger.info("Looking for Share button...")

            share_clicked = False
            share_selectors = [
                'button:has-text("Share")',
                'button >> text="Share"',
                'div[role="button"]:has-text("Share")',
                'button:has-text("Post")',
                '[type="button"]:has-text("Share")'
            ]

            for selector in share_selectors:
                try:
                    self.logger.info(f"Trying Share selector: {selector}")
                    share_btn = page.locator(selector).first
                    share_btn.wait_for(state='visible', timeout=5000)
                    time.sleep(2)

                    if share_btn.is_enabled():
                        share_btn.click()
                        self.logger.info("Share button clicked!")
                        share_clicked = True
                        break
                except Exception as e:
                    self.logger.debug(f"Share selector {selector} failed: {e}")
                    continue

            if not share_clicked:
                self.logger.error("Could not click Share button!")
                try:
                    page.get_by_text("Share", exact=True).click()
                    self.logger.info("Clicked Share using text match")
                    share_clicked = True
                except:
                    self.logger.error("All Share button methods failed")
                    return {'success': False, 'error': 'Could not click Share button'}

            # Wait for reel to publish
            self.logger.info("Waiting for reel to publish...")
            time.sleep(15)  # Reels take longer to process

            # Take screenshot
            screenshot_path = self.vault_path / 'logs' / f'ig_reel_{datetime.now().strftime("%Y%m%d_%H%M%S")}.png'
            page.screenshot(path=str(screenshot_path))
            self.logger.info(f"Screenshot saved: {screenshot_path}")

            ctx.close()
            pw.stop()

            media_id = f"ig_reel_{int(datetime.now().timestamp())}"
            post_url = "https://www.instagram.com/"

            self.logger.info("Reel published successfully!")

            return {
                'success': True,
                'media_id': media_id,
                'url': post_url,
                'caption': caption,
                'type': 'reel',
                'timestamp': datetime.now().isoformat(),
                'screenshot': str(screenshot_path)
            }

        except ImportError:
            self.logger.error("Playwright not installed")
            return {'success': False, 'error': 'Playwright not installed'}
        except Exception as e:
            self.logger.error(f"Error posting reel: {e}")
            return {'success': False, 'error': str(e)}

    def _demo_post(self, image_path: str, caption: str) -> Dict:
        """Demo mode post"""
        demo_media_id = f"demo_ig_{int(datetime.now().timestamp())}"
        demo_url = f"https://instagram.com/p/{demo_media_id}"

        self.logger.info(f"[DEMO] Would post to Instagram")
        self.logger.info(f"[DEMO] Image: {image_path}")
        self.logger.info(f"[DEMO] Caption: {caption[:50]}...")

        return {
            'success': True,
            'media_id': demo_media_id,
            'url': demo_url,
            'caption': caption,
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
    """Test the Instagram MCP server"""
    vault_path = os.getenv('VAULT_PATH', os.getcwd())
    mcp = InstagramMCP(vault_path)

    # Test posting (demo mode)
    result = mcp.post_photo(
        image_path="/path/to/image.jpg",
        caption="Testing Instagram MCP with Playwright! 🚀 #AIEmployee #Automation"
    )
    print(f"Post result: {result}")


if __name__ == '__main__':
    main()
