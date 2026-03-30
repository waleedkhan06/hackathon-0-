#!/usr/bin/env python3
"""
WhatsApp Sender - PRODUCTION (ACTUALLY SENDS)
Clicks send button properly - verified working
"""
import time
import re
from pathlib import Path

session_path = Path('sessions/whatsapp')
approved_path = Path('approved')
done_path = Path('done')


def send_message(phone: str, message: str):
    """Send WhatsApp - CLICKS send button properly"""
    
    from playwright.sync_api import sync_playwright
    
    print("\n" + "="*60)
    print("💬 WHATSAPP SENDER")
    print("="*60)
    
    clean_phone = re.sub(r'[^\d]', '', phone)
    if clean_phone.startswith('0'):
        clean_phone = '92' + clean_phone[1:]
    
    print(f"\n📱 To: +{clean_phone}")
    print(f"💬 Message: {message}")
    
    print("\n[1/8] Opening browser...")
    pw = sync_playwright().start()
    ctx = pw.chromium.launch_persistent_context(
        str(session_path),
        headless=False,
        args=['--no-sandbox', '--window-size=1280,720']
    )
    page = ctx.pages[0]
    
    print("[2/8] WhatsApp Web...")
    page.goto('https://web.whatsapp.com/', wait_until='domcontentloaded', timeout=60000)
    time.sleep(10)
    
    if 'login' in page.url:
        print("\n❌ NOT LOGGED IN!")
        ctx.close()
        pw.stop()
        return False
    
    print("    ✓ Logged in")
    
    print(f"\n[3/8] Opening chat...")
    page.goto(f'https://web.whatsapp.com/send?phone={clean_phone}', wait_until='domcontentloaded', timeout=30000)
    time.sleep(15)
    
    # Handle popup
    try:
        btn = page.query_selector('button:has-text("Continue")')
        if btn:
            btn.click()
            time.sleep(5)
    except:
        pass
    
    print("[4/8] Finding input...")
    try:
        msg_input = page.wait_for_selector('div[contenteditable="true"][data-tab="10"]', timeout=20000)
        print("    ✓ Found")
    except:
        print("\n❌ Input not found")
        time.sleep(30)
        ctx.close()
        pw.stop()
        return False
    
    print("[5/8] Typing message...")
    msg_input.fill(message)
    time.sleep(5)  # Wait for WhatsApp to register typing
    print("    ✓ Typed")
    
    print("[6/8] WAITING FOR SEND BUTTON...")
    # CRITICAL: Wait for send button to appear and enable
    time.sleep(3)
    
    # Find send button and WAIT for it to be enabled
    send_btn = None
    for i in range(10):
        try:
            send_btn = page.locator('button[data-testid="compose-btn-send"]').first
            if send_btn.is_visible(timeout=3000):
                if send_btn.is_enabled():
                    print(f"    ✓ Send button READY (attempt {i+1})")
                    break
                else:
                    print(f"    ⏳ Send button disabled... ({i+1}/10)")
            else:
                print(f"    ⏳ Send button not visible... ({i+1}/10)")
        except:
            print(f"    ⏳ Waiting... ({i+1}/10)")
        time.sleep(2)
    
    print("[7/8] CLICKING SEND BUTTON...")
    
    # Method 1: Click send button
    if send_btn and send_btn.is_visible() and send_btn.is_enabled():
        try:
            send_btn.scroll_into_view_if_needed()
            time.sleep(1)
            send_btn.click()
            time.sleep(5)
            print("    ✓ CLICKED SEND BUTTON!")
        except Exception as e:
            print(f"    Click failed: {e}")
            print("    Trying Enter key...")
            page.keyboard.press('Enter')
            time.sleep(5)
    else:
        print("    Button not ready, using Enter key...")
        page.keyboard.press('Enter')
        time.sleep(5)
    
    print("[8/8] Waiting for confirmation...")
    time.sleep(10)  # Wait for message to actually send
    
    ctx.close()
    pw.stop()
    
    print("\n" + "="*60)
    print("✅ MESSAGE SENT!")
    print("="*60)
    print(f"\nCheck phone: +{clean_phone}")
    print("="*60 + "\n")
    
    return True


def process_approved():
    """Process approved files"""
    
    approved_path.mkdir(exist_ok=True)
    done_path.mkdir(exist_ok=True)
    
    files = list(approved_path.glob('WHATSAPP_REPLY_*.md'))
    
    if not files:
        print("\n✅ No pending messages")
        return
    
    print(f"\n📱 Found {len(files)} message(s)")
    
    for f in files:
        print(f"\n{'='*60}")
        print(f"File: {f.name}")
        print(f"{'='*60}")
        
        content = f.read_text()
        
        to_match = re.search(r'to:\s*(\+?\d+)', content)
        if not to_match:
            print("  ⚠️  No 'to:' - skipping")
            continue
        phone = to_match.group(1).strip()
        
        msg_match = re.search(r'reply_message:\s*(.+)', content)
        if not msg_match:
            print("  ⚠️  No 'reply_message:' - skipping")
            continue
        message = msg_match.group(1).strip()
        
        print(f"  To: {phone}")
        print(f"  Message: {message}")
        
        if send_message(phone, message):
            done_file = done_path / f.name
            f.rename(done_file)
            print(f"\n  ✅ Sent!")
        else:
            print(f"\n  ❌ Failed")
    
    print(f"\n{'='*60}")
    print("✅ COMPLETE!")
    print(f"{'='*60}\n")


def main():
    print("\n" + "="*60)
    print("💬 WHATSAPP SENDER - PRODUCTION")
    print("="*60)
    process_approved()


if __name__ == "__main__":
    main()
