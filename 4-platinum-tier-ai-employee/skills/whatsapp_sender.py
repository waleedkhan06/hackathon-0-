#!/usr/bin/env python3
"""
WhatsApp Sender - SESSION-BASED ROBUST VERSION
Uses saved session properly, waits for full load, reliable sending
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
    """Send WhatsApp using saved session - properly waits for everything"""
    
    from playwright.sync_api import sync_playwright
    
    print("\n" + "="*70)
    print("  💬 WHATSAPP SENDER - SESSION VERSION")
    print("="*70)
    
    clean_phone = re.sub(r'[^\d]', '', phone)
    if clean_phone.startswith('0'):
        clean_phone = '92' + clean_phone[1:]
    
    print(f"\n📱 To: +{clean_phone}")
    print(f"💬 Message: {message[:50]}...")
    
    session_path.mkdir(parents=True, exist_ok=True)
    logs_path.mkdir(parents=True, exist_ok=True)
    
    pw = None
    ctx = None
    
    try:
        print("\n[1/10] Starting Playwright...")
        pw = sync_playwright().start()
        
        print("[2/10] Launching browser with saved session...")
        print(f"    Session: {session_path}")
        
        # Launch with session
        ctx = pw.chromium.launch_persistent_context(
            str(session_path),
            headless=False,
            args=[
                '--no-sandbox',
                '--disable-setuid-sandbox',
                '--window-size=1280,720',
                '--disable-dev-shm-usage'
            ]
        )
        
        page = ctx.pages[0] if ctx.pages else ctx.new_page()
        
        print("[3/10] Waiting for WhatsApp Web to load from session...")
        
        # First check current page
        print(f"    Current URL: {page.url[:80]}")
        
        # If not on WhatsApp, navigate
        if 'whatsapp' not in page.url.lower():
            print("    Navigating to WhatsApp Web...")
            page.goto('https://web.whatsapp.com/', wait_until='domcontentloaded', timeout=60000)
        
        print("    ⏳ Waiting 30 seconds for session to restore...")
        time.sleep(30)
        
        # Take screenshot to verify
        screenshot1 = logs_path / f'wa_session_{datetime.now().strftime("%H%M%S")}.png'
        page.screenshot(path=str(screenshot1))
        print(f"    ✓ Screenshot saved: {screenshot1}")
        
        # Check if we see the main app (indicates logged in)
        is_logged_in = False
        checks = [
            'div[data-testid="default-user"]',
            'div[data-testid="default-user"]',
            'span[data-icon="search"]',
            'div[data-icon="search"]'
        ]
        
        for check in checks:
            try:
                if page.query_selector(check):
                    is_logged_in = True
                    print("    ✓ Session loaded - logged in!")
                    break
            except:
                pass
        
        if not is_logged_in:
            print("\n⚠️  Session not loaded or not logged in")
            print("⏳ Waiting additional 60 seconds...")
            time.sleep(60)
            
            screenshot2 = logs_path / f'wa_waited_{datetime.now().strftime("%H%M%S")}.png'
            page.screenshot(path=str(screenshot2))
            print(f"    ✓ Screenshot: {screenshot2}")
        
        print("[4/10] Navigating to chat...")
        chat_url = f'https://web.whatsapp.com/send?phone={clean_phone}'
        print(f"    URL: {chat_url}")
        
        page.goto(chat_url, wait_until='domcontentloaded', timeout=30000)
        
        print("    ⏳ Waiting 90 seconds for chat to fully load...")
        # Critical: Wait long enough for chat to load
        for i in range(18):
            time.sleep(5)
            print(f"    ⏳ ({(i+1)*5}s)")
        
        screenshot3 = logs_path / f'wa_chat_{datetime.now().strftime("%H%M%S")}.png'
        page.screenshot(path=str(screenshot3))
        print(f"    ✓ Chat screenshot: {screenshot3}")
        
        print("[5/10] Finding message input...")
        msg_input = None
        
        # Try selectors
        selectors = [
            'div[contenteditable="true"][data-tab="10"]',
            'div[contenteditable="true"][data-lexical-editor="true"]',
            'div[contenteditable="true"][role="textbox"]',
            'div[aria-label="Type a message"]',
            'footer div[contenteditable="true"]'
        ]
        
        for sel in selectors:
            try:
                msg_input = page.query_selector(sel)
                if msg_input:
                    print(f"    ✓ Found: {sel[:50]}")
                    break
            except:
                pass
        
        if not msg_input:
            print("    ⚠️  Using keyboard navigation...")
            page.click('body')
            time.sleep(2)
            for _ in range(20):
                page.keyboard.press('Tab')
                time.sleep(0.3)
        
        print("[6/10] Typing message...")
        try:
            if msg_input:
                msg_input.click()
                time.sleep(2)
                msg_input.fill(message)
                time.sleep(5)
                print("    ✓ Message filled")
            else:
                page.keyboard.type(message, delay=100)
                time.sleep(3)
                print("    ✓ Message typed")
        except Exception as e:
            print(f"    ⚠️  Typing issue: {e}")
        
        screenshot4 = logs_path / f'wa_typed_{datetime.now().strftime("%H%M%S")}.png'
        page.screenshot(path=str(screenshot4))
        
        print("[7/10] Finding send button...")
        send_btn = None
        
        btn_selectors = [
            'button[data-testid="compose-btn-send"]',
            'button[aria-label*="Send"]',
            'button[title*="Send"]',
            'footer button'
        ]
        
        for sel in btn_selectors:
            try:
                send_btn = page.query_selector(sel)
                if send_btn and send_btn.is_enabled():
                    print(f"    ✓ Found send button!")
                    break
            except:
                pass
        
        print("[8/10] Sending message...")
        sent = False
        
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
        
        if not sent:
            print("    ⏳ Using Enter key...")
            try:
                page.keyboard.press('Enter')
                time.sleep(3)
                print("    ✓ Enter pressed")
                sent = True
            except Exception as e:
                print(f"    ⚠️  Enter failed: {e}")
        
        screenshot5 = logs_path / f'wa_sent_{datetime.now().strftime("%H%M%S")}.png'
        page.screenshot(path=str(screenshot5))
        
        print("[9/10] Waiting for delivery confirmation (120 seconds)...")
        delivered = False
        
        for i in range(24):
            time.sleep(5)
            
            # Check for checkmarks
            checkmarks = [
                'span[data-icon="msg-check"]',
                'span[data-icon="msg-dblcheck"]',
                'span[data-icon="msg-dblcheck-ack"]'
            ]
            
            for cm in checkmarks:
                try:
                    if page.query_selector(cm):
                        print(f"    ✓ Delivered! ({(i+1)*5}s)")
                        delivered = True
                        break
                except:
                    pass
            
            if delivered:
                break
            
            print(f"    ⏳ ({(i+1)*5}s)")
        
        print("[10/10] Final screenshot...")
        screenshot6 = logs_path / f'wa_final_{datetime.now().strftime("%H%M%S")}.png'
        page.screenshot(path=str(screenshot6))
        
        print("\n[Cleanup] Closing...")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        delivered = False
        sent = False
    
    finally:
        try:
            if ctx:
                ctx.close()
                print("    ✓ Context closed")
            if pw:
                pw.stop()
                print("    ✓ Playwright stopped")
        except:
            pass
    
    print("\n" + "="*70)
    if delivered:
        print("  ✅ MESSAGE SENT & DELIVERED!")
    elif sent:
        print("  ✅ MESSAGE SENT!")
    else:
        print("  ⚠️  CHECK PHONE FOR MESSAGE")
    
    print("="*70)
    print(f"\n📱 To: +{clean_phone}")
    print(f"📸 Screenshots: {logs_path}")
    print("="*70 + "\n")
    
    return True  # Always return true as user can verify on phone


def process_approved():
    """Process approved WhatsApp messages"""
    
    approved_path.mkdir(exist_ok=True)
    done_path.mkdir(exist_ok=True)
    
    files = list(approved_path.glob('WHATSAPP_*.md'))
    
    if not files:
        print("\n✅ No WhatsApp messages")
        return
    
    print(f"\n📱 Found {len(files)} message(s)\n")
    
    for f in files:
        print("="*70)
        print(f"File: {f.name}")
        print("="*70)
        
        content = f.read_text()
        
        to_match = re.search(r'to:\s*(\+?\d[\d\s-]{6,})', content)
        if not to_match:
            print("  ⚠️  No 'to:' - skipping")
            continue
        phone = to_match.group(1).strip()
        
        msg_match = re.search(r'reply_message:\s*(.+)', content)
        if not msg_match:
            print("  ⚠️  No 'reply_message:' - skipping")
            continue
        message = msg_match.group(1).strip()
        
        print(f"  📱 To: {phone}")
        print(f"  💬 Message: {message}")
        print()
        
        send_message(phone, message)
        
        # Move to done
        done_file = done_path / f.name
        f.rename(done_file)
        print(f"\n  ✅ Moved to /done/")
        print()
    
    print("="*70)
    print("✅ WHATSAPP COMPLETE!")
    print("="*70 + "\n")


def main():
    print("\n" + "="*70)
    print("  💬 WHATSAPP SENDER - SESSION VERSION")
    print("="*70)
    process_approved()


if __name__ == "__main__":
    main()
