#!/usr/bin/env python3
"""
WhatsApp Sender - DEBUG with Screenshots
Shows exactly what's happening at each step
"""
import time
import re
from pathlib import Path
from datetime import datetime

session_path = Path('sessions/whatsapp')
session_path.mkdir(parents=True, exist_ok=True)
logs_path = Path('logs')
logs_path.mkdir(exist_ok=True)

print("\n" + "="*60)
print("💬 WHATSAPP SENDER - DEBUG MODE")
print("="*60)

from playwright.sync_api import sync_playwright

# Test details
test_phone = "03352121689"
test_message = "DEBUG TEST - " + datetime.now().strftime("%H:%M:%S")

print(f"\n📱 To: {test_phone}")
print(f"💬 Message: {test_message}")

print("\n[1/8] Opening browser...")
pw = sync_playwright().start()
ctx = pw.chromium.launch_persistent_context(
    str(session_path),
    headless=False,
    args=['--no-sandbox', '--window-size=1280,720']
)
page = ctx.pages[0]

print("[2/8] Going to WhatsApp Web...")
page.goto('https://web.whatsapp.com/', wait_until='networkidle', timeout=60000)
time.sleep(5)

screenshot = logs_path / f'debug_01_login_{datetime.now().strftime("%H%M%S")}.png'
page.screenshot(path=str(screenshot))
print(f"    ✓ Screenshot: {screenshot.name}")

if 'login' in page.url:
    print("\n❌ NOT LOGGED IN!")
    ctx.close()
    pw.stop()
    exit(1)

print("    ✓ Logged in!")

print("\n[3/8] Opening chat...")
clean_phone = re.sub(r'[^\d]', '', test_phone)
if clean_phone.startswith('0'):
    clean_phone = '92' + clean_phone[1:]

page.goto(f'https://web.whatsapp.com/send?phone={clean_phone}', wait_until='networkidle', timeout=30000)
time.sleep(10)

screenshot = logs_path / f'debug_02_chat_{datetime.now().strftime("%H%M%S")}.png'
page.screenshot(path=str(screenshot))
print(f"    ✓ Screenshot: {screenshot.name}")

# Handle popup
try:
    continue_btn = page.query_selector('button:has-text("Continue")')
    if continue_btn:
        continue_btn.click()
        time.sleep(3)
        print("    ✓ Handled popup")
        screenshot = logs_path / f'debug_03_popup_{datetime.now().strftime("%H%M%S")}.png'
        page.screenshot(path=str(screenshot))
except:
    pass

print("\n[4/8] Finding message input...")
try:
    message_input = page.wait_for_selector(
        'div[contenteditable="true"][data-tab="10"]',
        timeout=15000
    )
    print("    ✓ Input found")
except:
    print("\n❌ Input not found!")
    print("Check screenshots in logs/")
    ctx.close()
    pw.stop()
    exit(1)

print("\n[5/8] Typing message...")
message_input.fill(test_message)
time.sleep(3)

screenshot = logs_path / f'debug_04_typed_{datetime.now().strftime("%H%M%S")}.png'
page.screenshot(path=str(screenshot))
print(f"    ✓ Screenshot: {screenshot.name}")
print("    ✓ Message typed")

print("\n[6/8] Checking send button...")
send_button = page.locator('button[data-testid="compose-btn-send"]').first
try:
    is_visible = send_button.is_visible(timeout=5000)
    is_enabled = send_button.is_enabled()
    print(f"    Send button visible: {is_visible}")
    print(f"    Send button enabled: {is_enabled}")
    
    screenshot = logs_path / f'debug_05_sendbtn_{datetime.now().strftime("%H%M%S")}.png'
    page.screenshot(path=str(screenshot))
    print(f"    ✓ Screenshot: {screenshot.name}")
except Exception as e:
    print(f"    Send button error: {e}")

print("\n[7/8] Sending message...")
print("    Method 1: Clicking send button...")
try:
    send_button.click()
    time.sleep(2)
    print("    ✓ Clicked send button")
except Exception as e:
    print(f"    Click failed: {e}")
    print("    Method 2: Using Enter key...")
    page.keyboard.press('Enter')
    time.sleep(2)
    print("    ✓ Pressed Enter")

screenshot = logs_path / f'debug_06_sent_{datetime.now().strftime("%H%M%S")}.png'
page.screenshot(path=str(screenshot))
print(f"    ✓ Screenshot: {screenshot.name}")

print("\n[8/8] Waiting for send confirmation...")
print("    ⏳ Waiting 15 seconds...")
time.sleep(15)

screenshot = logs_path / f'debug_07_final_{datetime.now().strftime("%H%M%S")}.png'
page.screenshot(path=str(screenshot))
print(f"    ✓ Final screenshot: {screenshot.name}")

ctx.close()
pw.stop()

print("\n" + "="*60)
print("✅ DEBUG COMPLETE!")
print("="*60)
print(f"\n📸 Check screenshots in: {logs_path}")
print("   Look for files starting with 'debug_'")
print("\n📱 Check your phone for the message!")
print("="*60 + "\n")
