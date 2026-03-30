#!/usr/bin/env python3
"""
WhatsApp Sender - ROBUST PRODUCTION VERSION
Fixed: Chat loading, session handling, send button detection
"""

import time
import re
from pathlib import Path
from datetime import datetime

session_path = Path('sessions/whatsapp')
approved_path = Path('approved')
done_path = Path('done')
logs_path = Path('logs')


def send_message(phone: str, message: str):
    """Send WhatsApp message - Robust version with better error handling"""
    
    from playwright.sync_api import sync_playwright
    
    print("\n" + "="*70)
    print("  💬 WHATSAPP SENDER - ROBUST VERSION")
    print("="*70)
    
    # Clean phone number
    clean_phone = re.sub(r'[^\d]', '', phone)
    if clean_phone.startswith('0'):
        clean_phone = '92' + clean_phone[1:]
    
    print(f"\n📱 To: +{clean_phone}")
    print(f"💬 Message: {message[:50]}...")
    print(f"⏱️  Timeout: 180 seconds")
    
    # Ensure session and logs directories exist
    session_path.mkdir(parents=True, exist_ok=True)
    logs_path.mkdir(parents=True, exist_ok=True)
    
    print("\n[1/10] Initializing browser...")
    try:
        pw = sync_playwright().start()
    except Exception as e:
        print(f"❌ Failed to start Playwright: {e}")
        return False
    
    print("[2/10] Launching browser with session...")
    try:
        ctx = pw.chromium.launch_persistent_context(
            str(session_path),
            headless=False,
            args=[
                '--no-sandbox',
                '--disable-setuid-sandbox',
                '--window-size=1280,720',
                '--disable-dev-shm-usage',
                '--disable-accelerated-2d-canvas',
                '--disable-gpu'
            ]
        )
        page = ctx.pages[0] if ctx.pages else ctx.new_page()
    except Exception as e:
        print(f"❌ Failed to launch browser: {e}")
        pw.stop()
        return False
    
    print("[3/10] Loading WhatsApp Web...")
    try:
        page.goto('https://web.whatsapp.com/', wait_until='domcontentloaded', timeout=60000)
        print("    ⏳ Waiting for page to load...")
        time.sleep(15)  # Give extra time for WhatsApp to initialize
        
        # Take screenshot for debugging
        screenshot = logs_path / f'whatsapp_loaded_{datetime.now().strftime("%H%M%S")}.png'
        page.screenshot(path=str(screenshot))
        print(f"    ✓ Screenshot saved: {screenshot}")
        
    except Exception as e:
        print(f"❌ Failed to load WhatsApp: {e}")
        ctx.close()
        pw.stop()
        return False
    
    # Check if logged in
    current_url = page.url.lower()
    if 'login' in current_url or 'qr' in current_url:
        print("\n⚠️  NOT LOGGED IN - Please scan QR code")
        print("⏳ Waiting 60 seconds for login...")
        
        try:
            # Wait for main app to appear (indicates login)
            page.wait_for_selector('div[data-testid="default-user"]', timeout=60000)
            print("    ✓ Logged in successfully!")
        except:
            print("❌ Login timeout - please scan QR code and try again")
            ctx.close()
            pw.stop()
            return False
    
    print("[4/10] Navigating to chat...")
    # Use wa.me link which is more reliable
    wa_link = f'https://web.whatsapp.com/send?phone={clean_phone}&text={message[:50]}'
    
    try:
        page.goto(wa_link, wait_until='domcontentloaded', timeout=30000)
        print("    ⏳ Waiting for chat to load (45 seconds)...")
        
        # Wait longer for chat to fully load
        time.sleep(45)
        
        # Take another screenshot
        screenshot2 = logs_path / f'whatsapp_chat_{datetime.now().strftime("%H%M%S")}.png'
        page.screenshot(path=str(screenshot2))
        print(f"    ✓ Chat screenshot: {screenshot2}")
        
    except Exception as e:
        print(f"⚠️  Navigation issue: {e}")
    
    # Close any popups
    print("[5/10] Checking for popups...")
    try:
        # Close "Continue" popup if appears
        continue_btn = page.query_selector('button:has-text("Continue"), button:has-text("Got it")')
        if continue_btn:
            continue_btn.click()
            print("    ✓ Closed popup")
            time.sleep(3)
    except:
        print("    ✓ No popups found")
    
    print("[6/10] Finding message input...")
    msg_input = None
    
    # Try multiple selectors with longer timeouts
    selectors = [
        'div[contenteditable="true"][data-tab="10"]',
        'div[contenteditable="true"][data-lexical-editor="true"]',
        'div[contenteditable="true"][role="textbox"]',
        'div[aria-label="Type a message"]',
        'footer div[contenteditable="true"]'
    ]
    
    for i, selector in enumerate(selectors, 1):
        try:
            print(f"    Trying selector {i}: {selector[:50]}")
            msg_input = page.wait_for_selector(selector, timeout=8000)
            if msg_input:
                print(f"    ✓ Found input field!")
                break
        except:
            continue
    
    # Fallback: keyboard navigation
    if not msg_input:
        print("    ⚠️  Using keyboard fallback...")
        page.click('body')
        time.sleep(2)
        for _ in range(15):
            page.keyboard.press('Tab')
            time.sleep(0.3)
        print("    ✓ Keyboard navigation complete")
    
    print("[7/10] Typing message...")
    if msg_input:
        try:
            msg_input.click()
            time.sleep(2)
            msg_input.fill('')  # Clear any existing text
            time.sleep(1)
            msg_input.fill(message)  # Fill with our message
            time.sleep(5)  # Wait for WhatsApp to process
            print("    ✓ Message typed via fill")
        except:
            page.keyboard.type(message, delay=50)
            time.sleep(3)
            print("    ✓ Message typed via keyboard")
    else:
        page.keyboard.type(message, delay=50)
        time.sleep(3)
        print("    ✓ Message typed (fallback)")
    
    print("[8/10] Finding send button...")
    send_btn = None
    
    send_selectors = [
        'button[data-testid="compose-btn-send"]',
        'button[aria-label*="Send"]',
        'button[title*="Send"]',
        'footer button'
    ]
    
    for i, selector in enumerate(send_selectors, 1):
        try:
            print(f"    Trying send selector {i}: {selector[:50]}")
            send_btn = page.wait_for_selector(selector, timeout=5000)
            if send_btn and send_btn.is_enabled():
                print(f"    ✓ Found send button!")
                break
        except:
            continue
    
    print("[9/10] Sending message...")
    sent = False
    
    # Method 1: Click send button
    if send_btn:
        try:
            send_btn.scroll_into_view_if_needed()
            time.sleep(2)
            send_btn.click(force=True)
            time.sleep(3)
            print("    ✓ Send button clicked!")
            sent = True
        except Exception as e:
            print(f"    ⚠️  Click failed: {e}")
    
    # Method 2: Enter key
    if not sent:
        print("    ⏳ Using Enter key...")
        try:
            page.keyboard.press('Enter')
            time.sleep(3)
            print("    ✓ Enter pressed!")
            sent = True
        except:
            print("    ⚠️  Enter key failed")
    
    print("[10/10] Waiting for delivery confirmation...")
    print("    ⏳ Monitoring for 90 seconds...")
    
    delivered = False
    for i in range(18):  # Check every 5 seconds for 90 seconds
        time.sleep(5)
        
        # Check for checkmarks (delivered)
        checkmarks = [
            'span[data-icon="msg-check"]',      # Single check
            'span[data-icon="msg-dblcheck"]',   # Double check
            'span[data-icon="msg-dblcheck-ack"]'  # Blue double check
        ]
        
        for cm in checkmarks:
            try:
                if page.query_selector(cm):
                    print(f"    ✓ Message delivered! ({(i+1)*5}s)")
                    delivered = True
                    break
            except:
                continue
        
        if delivered:
            break
        
        # Check for error
        try:
            if page.query_selector('span[data-icon="error-msg"]'):
                print("    ⚠️  Message failed - retrying...")
                page.keyboard.press('Enter')
                time.sleep(10)
        except:
            pass
        
        print(f"    ⏳ Waiting... ({(i+1)*5}s)")
    
    # Cleanup
    print("\n[Cleanup] Closing browser...")
    ctx.close()
    pw.stop()
    print("    ✓ Browser closed")
    
    # Final result
    print("\n" + "="*70)
    if delivered:
        print("  ✅ MESSAGE SENT SUCCESSFULLY!")
        print("="*70)
        print(f"\n📱 To: +{clean_phone}")
        print(f"💬 Message: {message[:50]}...")
        print(f"⏱️  Total time: ~{(i+1)*5} seconds")
        print("="*70 + "\n")
        return True
    elif sent:
        print("  ⚠️  MESSAGE SENT (awaiting delivery confirmation)")
        print("="*70)
        print(f"\n📱 To: +{clean_phone}")
        print("Check your phone to verify delivery")
        print("="*70 + "\n")
        return True  # Consider it success if we sent it
    else:
        print("  ❌ MESSAGE NOT SENT")
        print("="*70)
        print("\nTroubleshooting:")
        print("1. Check if you're logged into WhatsApp Web")
        print("2. Verify the phone number is correct")
        print("3. Check your internet connection")
        print("4. Try again in a few minutes")
        print("="*70 + "\n")
        return False


def process_approved():
    """Process approved WhatsApp messages"""
    
    approved_path.mkdir(exist_ok=True)
    done_path.mkdir(exist_ok=True)
    
    # Find all WhatsApp reply files
    files = list(approved_path.glob('WHATSAPP_*.md'))
    
    if not files:
        print("\n✅ No WhatsApp messages to send")
        return
    
    print(f"\n📱 Found {len(files)} WhatsApp message(s)")
    
    for f in files:
        print(f"\n{'='*70}")
        print(f"File: {f.name}")
        print(f"{'='*70}")
        
        content = f.read_text()
        
        # Extract phone number
        to_match = re.search(r'to:\s*(\+?\d[\d\s-]{6,})', content)
        if not to_match:
            print("  ⚠️  No 'to:' field found - skipping")
            continue
        phone = to_match.group(1).strip()
        
        # Extract message
        msg_match = re.search(r'reply_message:\s*(.+)', content)
        if not msg_match:
            print("  ⚠️  No 'reply_message:' field found - skipping")
            continue
        message = msg_match.group(1).strip()
        
        print(f"  📱 To: {phone}")
        print(f"  💬 Message: {message}")
        
        # Send the message
        if send_message(phone, message):
            done_file = done_path / f.name
            f.rename(done_file)
            print(f"\n  ✅ Message sent! File moved to /done/")
        else:
            print(f"\n  ❌ Failed to send message")
    
    print(f"\n{'='*70}")
    print("✅ WHATSAPP SENDER COMPLETE!")
    print(f"{'='*70}\n")


def main():
    """Main entry point"""
    print("\n" + "="*70)
    print("  💬 WHATSAPP SENDER - ROBUST PRODUCTION VERSION")
    print("="*70)
    process_approved()


if __name__ == "__main__":
    main()
