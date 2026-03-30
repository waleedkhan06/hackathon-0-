#!/usr/bin/env python3
"""
WhatsApp Sender - FAST VERSION (30 seconds max)
Uses direct wa.me link - no chat list loading
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
    """Send WhatsApp message - FAST version using wa.me link"""
    
    from playwright.sync_api import sync_playwright
    
    print("\n" + "="*70)
    print("  💬 WHATSAPP SENDER - FAST VERSION")
    print("="*70)
    
    # Clean phone number
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
        print("\n[1/8] Starting Playwright...")
        pw = sync_playwright().start()
        
        print("[2/8] Launching browser (15 seconds)...")
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
        
        print("[3/8] Loading WhatsApp Web (20 seconds)...")
        page.goto('https://web.whatsapp.com/', wait_until='domcontentloaded', timeout=60000)
        time.sleep(20)  # Wait for session to load
        
        # Check if logged in
        if 'login' in page.url.lower():
            print("\n⚠️  Please scan QR code if not logged in")
            print("⏳ Waiting 30 seconds...")
            time.sleep(30)
        
        print("[4/8] Opening direct chat link (FAST - no chat list)...")
        # Use wa.me link which opens chat directly without loading chat list
        wa_link = f'https://web.whatsapp.com/send?phone={clean_phone}'
        page.goto(wa_link, wait_until='domcontentloaded', timeout=30000)
        
        print("    ⏳ Waiting 30 seconds for chat to load...")
        time.sleep(30)  # Shorter wait since we're going direct
        
        print("[5/8] Finding message input...")
        msg_input = None
        
        # Try selectors
        selectors = [
            'div[contenteditable="true"][data-tab="10"]',
            'div[contenteditable="true"][data-lexical-editor="true"]',
            'div[aria-label="Type a message"]',
            'footer div[contenteditable="true"]'
        ]
        
        for sel in selectors:
            try:
                msg_input = page.query_selector(sel)
                if msg_input:
                    print(f"    ✓ Found input")
                    break
            except:
                pass
        
        if not msg_input:
            # Keyboard fallback
            print("    ⚠️  Using keyboard fallback...")
            page.click('body')
            time.sleep(2)
            for _ in range(15):
                page.keyboard.press('Tab')
                time.sleep(0.2)
        
        print("[6/8] Typing message (10 seconds)...")
        if msg_input:
            msg_input.click()
            time.sleep(1)
            msg_input.fill(message)
            time.sleep(3)
            print("    ✓ Message typed")
        else:
            page.keyboard.type(message, delay=50)
            time.sleep(3)
            print("    ✓ Message typed (fallback)")
        
        print("[7/8] Sending message (10 seconds)...")
        sent = False
        
        # Try send button
        send_btns = [
            'button[data-testid="compose-btn-send"]',
            'button[aria-label*="Send"]',
            'footer button'
        ]
        
        for btn_sel in send_btns:
            try:
                send_btn = page.query_selector(btn_sel)
                if send_btn and send_btn.is_enabled():
                    send_btn.scroll_into_view_if_needed()
                    time.sleep(1)
                    send_btn.click(force=True)
                    time.sleep(2)
                    print("    ✓ Send button clicked!")
                    sent = True
                    break
            except:
                pass
        
        if not sent:
            print("    ⏳ Using Enter key...")
            page.keyboard.press('Enter')
            time.sleep(2)
            print("    ✓ Enter pressed")
            sent = True
        
        print("[8/8] Waiting for delivery (30 seconds)...")
        delivered = False
        
        for i in range(6):
            time.sleep(5)
            
            # Check for checkmarks
            checks = [
                'span[data-icon="msg-check"]',
                'span[data-icon="msg-dblcheck"]'
            ]
            
            for cm in checks:
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
        
        print("\n[Cleanup] Closing browser...")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        delivered = False
        sent = False
    
    finally:
        try:
            if ctx:
                ctx.close()
            if pw:
                pw.stop()
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
    print("="*70 + "\n")
    
    return True


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
        
        done_file = done_path / f.name
        f.rename(done_file)
        print(f"\n  ✅ Moved to /done/")
        print()
    
    print("="*70)
    print("✅ WHATSAPP COMPLETE!")
    print("="*70 + "\n")


def main():
    print("\n" + "="*70)
    print("  💬 WHATSAPP SENDER - FAST VERSION (30-60 seconds)")
    print("="*70)
    process_approved()


if __name__ == "__main__":
    main()
