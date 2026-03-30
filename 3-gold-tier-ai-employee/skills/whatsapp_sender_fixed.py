#!/usr/bin/env python3
"""
WhatsApp Sender - FIXED & ROBUST
Properly handles: browser lifecycle, chat loading, message sending
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
    """Send WhatsApp message - completely fixed version"""
    
    from playwright.sync_api import sync_playwright
    
    print("\n" + "="*70)
    print("  💬 WHATSAPP SENDER - FIXED VERSION")
    print("="*70)
    
    # Clean phone number
    clean_phone = re.sub(r'[^\d]', '', phone)
    if clean_phone.startswith('0'):
        clean_phone = '92' + clean_phone[1:]
    
    print(f"\n📱 To: +{clean_phone}")
    print(f"💬 Message: {message[:50]}...")
    
    # Ensure directories exist
    session_path.mkdir(parents=True, exist_ok=True)
    logs_path.mkdir(parents=True, exist_ok=True)
    
    pw = None
    ctx = None
    page = None
    
    try:
        print("\n[1/12] Starting Playwright...")
        pw = sync_playwright().start()
        
        print("[2/12] Launching browser...")
        ctx = pw.chromium.launch_persistent_context(
            str(session_path),
            headless=False,
            args=[
                '--no-sandbox',
                '--disable-setuid-sandbox',
                '--window-size=1280,720',
                '--disable-dev-shm-usage',
                '--disable-gpu'
            ]
        )
        page = ctx.pages[0] if ctx.pages else ctx.new_page()
        
        print("[3/12] Loading WhatsApp Web...")
        page.goto('https://web.whatsapp.com/', wait_until='domcontentloaded', timeout=60000)
        print("    ⏳ Waiting 20 seconds for initialization...")
        time.sleep(20)
        
        # Check if logged in
        if 'login' in page.url.lower():
            print("\n⚠️  Please scan QR code if not logged in")
            print("⏳ Waiting 60 seconds...")
            time.sleep(60)
        
        print("[4/12] Taking screenshot...")
        screenshot1 = logs_path / f'wa_before_{datetime.now().strftime("%H%M%S")}.png'
        page.screenshot(path=str(screenshot1))
        
        print("[5/12] Opening chat with phone number...")
        # Direct URL to chat
        chat_url = f'https://web.whatsapp.com/send?phone={clean_phone}'
        page.goto(chat_url, wait_until='domcontentloaded', timeout=30000)
        
        print("    ⏳ Waiting 60 seconds for chat to load...")
        # WhatsApp needs time to load the chat
        for i in range(12):
            time.sleep(5)
            print(f"    ⏳ Loading... ({(i+1)*5}s)")
        
        print("[6/12] Taking chat screenshot...")
        screenshot2 = logs_path / f'wa_chat_{datetime.now().strftime("%H%M%S")}.png'
        page.screenshot(path=str(screenshot2))
        
        print("[7/12] Closing any popups...")
        try:
            # Try to close common popups
            popups = [
                'button:has-text("Continue")',
                'button:has-text("Got it")',
                'button:has-text("OK")'
            ]
            for popup_sel in popups:
                btn = page.query_selector(popup_sel)
                if btn:
                    btn.click()
                    print(f"    ✓ Closed popup: {popup_sel}")
                    time.sleep(2)
        except:
            print("    ✓ No popups")
        
        print("[8/12] Finding message input field...")
        msg_input = None
        
        # Multiple selector attempts
        selectors = [
            'div[contenteditable="true"][data-tab="10"]',
            'div[contenteditable="true"][data-lexical-editor="true"]',
            'div[contenteditable="true"][role="textbox"]',
            'div[aria-label="Type a message"]',
            'footer div[contenteditable="true"]',
            'div[title="Type a message"]'
        ]
        
        for sel in selectors:
            try:
                msg_input = page.query_selector(sel)
                if msg_input:
                    print(f"    ✓ Found: {sel[:50]}")
                    break
            except:
                continue
        
        if not msg_input:
            print("    ⚠️  Using keyboard fallback...")
            page.click('body')
            time.sleep(2)
            for _ in range(20):
                page.keyboard.press('Tab')
                time.sleep(0.2)
        
        print("[9/12] Typing message...")
        try:
            if msg_input:
                msg_input.click()
                time.sleep(2)
                # Type in chunks to avoid issues
                msg_input.fill(message)
                time.sleep(5)
                print("    ✓ Message filled")
            else:
                page.keyboard.type(message, delay=100)
                time.sleep(3)
                print("    ✓ Message typed")
        except Exception as e:
            print(f"    ⚠️  Typing issue: {e}")
            # Fallback: use clipboard
            page.evaluate(f'navigator.clipboard.writeText("{message}")')
            page.keyboard.press('Control+v')
            time.sleep(2)
        
        print("[10/12] Taking typing screenshot...")
        screenshot3 = logs_path / f'wa_typing_{datetime.now().strftime("%H%M%S")}.png'
        page.screenshot(path=str(screenshot3))
        
        print("[11/12] Sending message...")
        sent = False
        
        # Try send button
        send_btns = [
            'button[data-testid="compose-btn-send"]',
            'button[aria-label*="Send"]',
            'button[title*="Send"]',
            'footer button[aria-label]'
        ]
        
        for btn_sel in send_btns:
            try:
                send_btn = page.query_selector(btn_sel)
                if send_btn and send_btn.is_enabled():
                    send_btn.scroll_into_view_if_needed()
                    time.sleep(2)
                    send_btn.click(force=True)
                    time.sleep(3)
                    print(f"    ✓ Sent via button: {btn_sel[:40]}")
                    sent = True
                    break
            except:
                continue
        
        # Fallback: Enter key
        if not sent:
            print("    ⏳ Using Enter key...")
            try:
                page.keyboard.press('Enter')
                time.sleep(3)
                print("    ✓ Enter pressed")
                sent = True
            except Exception as e:
                print(f"    ⚠️  Enter failed: {e}")
        
        print("[12/12] Waiting for delivery (90 seconds)...")
        delivered = False
        
        for i in range(18):
            time.sleep(5)
            
            # Check for delivery indicators
            checks = [
                'span[data-icon="msg-check"]',
                'span[data-icon="msg-dblcheck"]',
                'span[data-icon="msg-dblcheck-ack"]'
            ]
            
            for check in checks:
                try:
                    if page.query_selector(check):
                        print(f"    ✓ Delivered! ({(i+1)*5}s)")
                        delivered = True
                        break
                except:
                    pass
            
            if delivered:
                break
            
            print(f"    ⏳ Waiting... ({(i+1)*5}s)")
        
        # Final screenshot
        screenshot4 = logs_path / f'wa_final_{datetime.now().strftime("%H%M%S")}.png'
        page.screenshot(path=str(screenshot4))
        
        print("\n[Cleanup] Closing browser...")
        
    except Exception as e:
        print(f"\n❌ Error during execution: {e}")
        delivered = False
        sent = False
    
    finally:
        # Always cleanup
        try:
            if ctx:
                ctx.close()
                print("    ✓ Context closed")
            if pw:
                pw.stop()
                print("    ✓ Playwright stopped")
        except:
            pass
    
    # Result
    print("\n" + "="*70)
    if delivered:
        print("  ✅ MESSAGE SENT & DELIVERED!")
    elif sent:
        print("  ✅ MESSAGE SENT (awaiting delivery)")
    else:
        print("  ⚠️  MESSAGE STATUS UNKNOWN")
    
    print("="*70)
    print(f"\n📱 To: +{clean_phone}")
    print(f"💬 Message: {message[:50]}...")
    print(f"📸 Screenshots saved to: {logs_path}")
    print("="*70 + "\n")
    
    return sent or delivered


def process_approved():
    """Process all approved WhatsApp messages"""
    
    approved_path.mkdir(exist_ok=True)
    done_path.mkdir(exist_ok=True)
    
    # Find WhatsApp files
    files = list(approved_path.glob('WHATSAPP_*.md'))
    
    if not files:
        print("\n✅ No WhatsApp messages to send")
        return
    
    print(f"\n📱 Found {len(files)} WhatsApp message(s)\n")
    
    success_count = 0
    
    for f in files:
        print("="*70)
        print(f"File: {f.name}")
        print("="*70)
        
        content = f.read_text()
        
        # Extract phone
        to_match = re.search(r'to:\s*(\+?\d[\d\s-]{6,})', content)
        if not to_match:
            print("  ⚠️  No 'to:' field - skipping")
            continue
        phone = to_match.group(1).strip()
        
        # Extract message
        msg_match = re.search(r'reply_message:\s*(.+)', content)
        if not msg_match:
            print("  ⚠️  No 'reply_message:' field - skipping")
            continue
        message = msg_match.group(1).strip()
        
        print(f"  📱 To: {phone}")
        print(f"  💬 Message: {message}")
        print()
        
        # Send
        if send_message(phone, message):
            done_file = done_path / f.name
            f.rename(done_file)
            print(f"\n  ✅ SUCCESS! Moved to /done/")
            success_count += 1
        else:
            print(f"\n  ⚠️  Check phone for message status")
        
        print()
    
    print("="*70)
    print(f"✅ COMPLETE: {success_count}/{len(files)} messages sent")
    print("="*70 + "\n")


def main():
    """Main entry point"""
    print("\n" + "="*70)
    print("  💬 WHATSAPP SENDER - FIXED PRODUCTION VERSION")
    print("="*70)
    process_approved()


if __name__ == "__main__":
    main()
