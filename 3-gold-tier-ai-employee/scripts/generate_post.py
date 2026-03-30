#!/usr/bin/env python3
"""
AI Employee Post Generator
Creates editable post templates in /pending_approval/

Usage: python3 scripts/generate_post.py <platform>

Platforms: email, facebook, instagram, linkedin, whatsapp, all
"""

import sys
import os
from pathlib import Path
from datetime import datetime

project_root = Path(__file__).parent.parent
pending_approval = project_root / 'pending_approval'
pending_approval.mkdir(exist_ok=True)


def generate_email():
    """Generate email post template"""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f'EMAIL_POST_{timestamp}.md'
    filepath = pending_approval / filename
    
    content = f"""---
type: approval_request
action: email_send
to: [RECIPIENT_EMAIL]
subject: [YOUR_SUBJECT_HERE]
created: {datetime.now().isoformat()}
status: pending
priority: medium
---

# Email - EDIT BEFORE APPROVING

## Instructions
1. Edit the [BRACKETED] fields above
2. Write your email content below
3. Save the file
4. Move to /approved/ to send

## Email Content

[Write your email content here...]

---

## To Approve
1. Edit this file with your content
2. **Move to /approved/ folder**
3. Email will be sent automatically

## To Reject
Delete this file or move to /rejected/
"""
    
    filepath.write_text(content, encoding='utf-8')
    print(f"\n✅ Email template created: {filename}")
    print(f"📁 Location: pending_approval/")
    print(f"✏️  Edit the file with your content")
    print(f"👉 Move to /approved/ when ready to send")
    return filepath


def generate_facebook():
    """Generate Facebook post template"""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f'FACEBOOK_POST_{timestamp}.md'
    filepath = pending_approval / filename
    
    content = f"""---
type: approval_request
action: facebook_post
platform: facebook
created: {datetime.now().isoformat()}
status: pending
priority: medium
---

# Facebook Post - EDIT BEFORE APPROVING

## Instructions
1. Write your Facebook post content below
2. Add relevant hashtags
3. Save the file
4. Move to /approved/ to post

## Post Content

[Write your Facebook post here...]

Example:
🎉 Exciting news from our company!

We're thrilled to announce...

#YourHashtags #Here

---

## To Approve
1. Edit this file with your content
2. **Move to /approved/ folder**
3. Post will be published automatically (~4 seconds)

## To Reject
Delete this file or move to /rejected/
"""
    
    filepath.write_text(content, encoding='utf-8')
    print(f"\n✅ Facebook template created: {filename}")
    print(f"📁 Location: pending_approval/")
    print(f"✏️  Edit the file with your content")
    print(f"👉 Move to /approved/ when ready to post")
    return filepath


def generate_instagram():
    """Generate Instagram post template"""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f'INSTAGRAM_POST_{timestamp}.md'
    filepath = pending_approval / filename
    
    content = f"""---
type: approval_request
action: instagram_post
platform: instagram
image_url: [PASTE_IMAGE_URL_HERE]
created: {datetime.now().isoformat()}
status: pending
priority: medium
---

# Instagram Post - EDIT BEFORE APPROVING

## Instructions
1. Add image URL (must be publicly accessible)
2. Write your caption below
3. Add hashtags
4. Save the file
5. Move to /approved/ to post

## Image URL
[Paste direct image URL here - must be public]
Example: https://images.unsplash.com/photo-1234567890

## Caption

[Write your Instagram caption here...]

Example:
📸 Beautiful moment captured!

Double tap if you agree ❤️

#Instagram #Photography #YourHashtags

---

## To Approve
1. Edit this file with image URL and caption
2. **Move to /approved/ folder**
3. Post will be published automatically (~10 seconds)

## To Reject
Delete this file or move to /rejected/

⚠️ Note: Instagram requires a publicly accessible image URL
"""
    
    filepath.write_text(content, encoding='utf-8')
    print(f"\n✅ Instagram template created: {filename}")
    print(f"📁 Location: pending_approval/")
    print(f"✏️  Edit the file with image URL and caption")
    print(f"👉 Move to /approved/ when ready to post")
    return filepath


def generate_linkedin():
    """Generate LinkedIn post template"""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f'LINKEDIN_POST_{timestamp}.md'
    filepath = pending_approval / filename
    
    content = f"""---
type: approval_request
action: linkedin_post
platform: linkedin
created: {datetime.now().isoformat()}
status: pending
priority: medium
---

# LinkedIn Post - EDIT BEFORE APPROVING

## Instructions
1. Write your professional LinkedIn post
2. Keep it professional and engaging
3. Add relevant hashtags
4. Save the file
5. Move to /approved/ then run post_linkedin.py

## Post Content

[Write your LinkedIn post here...]

Example:
🚀 Professional Update

I'm excited to share that...

Key highlights:
✅ Achievement 1
✅ Achievement 2
✅ Achievement 3

#Professional #Business #Industry #Hashtags

---

## To Approve
1. Edit this file with your content
2. **Move to /approved/ folder**
3. Run: python3 post_linkedin.py
4. Browser will open and post automatically

## To Reject
Delete this file or move to /rejected/

⚠️ Note: LinkedIn posting uses browser automation (60-90 seconds)
"""
    
    filepath.write_text(content, encoding='utf-8')
    print(f"\n✅ LinkedIn template created: {filename}")
    print(f"📁 Location: pending_approval/")
    print(f"✏️  Edit the file with your content")
    print(f"👉 Move to /approved/, then run: python3 post_linkedin.py")
    return filepath


def generate_whatsapp():
    """Generate WhatsApp message template"""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f'WHATSAPP_MESSAGE_{timestamp}.md'
    filepath = pending_approval / filename
    
    content = f"""---
type: approval_request
action: whatsapp_send
to: [PHONE_NUMBER]
created: {datetime.now().isoformat()}
status: pending
priority: medium
---

# WhatsApp Message - EDIT BEFORE APPROVING

## Instructions
1. Add phone number (with country code, e.g., +923001234567)
2. Write your message (keep it short - under 160 chars recommended)
3. No emojis recommended (can cause issues)
4. Save the file
5. Move to /approved/ then run whatsapp sender

## Recipient
**Phone:** [Enter phone number with country code]
Example: +923001234567

## Message

[Write your WhatsApp message here...]

Keep it short and simple!
No emojis recommended.

---

## To Approve
1. Edit this file with phone number and message
2. **Move to /approved/ folder**
3. Run: python3 skills/whatsapp_sender.py
4. Message will be sent via WhatsApp Web

## To Reject
Delete this file or move to /rejected/

⚠️ Note: WhatsApp uses browser automation. Keep messages short (<100 chars, no emojis).
"""
    
    filepath.write_text(content, encoding='utf-8')
    print(f"\n✅ WhatsApp template created: {filename}")
    print(f"📁 Location: pending_approval/")
    print(f"✏️  Edit the file with phone number and message")
    print(f"👉 Move to /approved/, then run: python3 skills/whatsapp_sender.py")
    return filepath


def generate_all():
    """Generate templates for all platforms"""
    print("\n" + "=" * 70)
    print("  GENERATING ALL POST TEMPLATES")
    print("=" * 70)
    
    generate_email()
    generate_facebook()
    generate_instagram()
    generate_linkedin()
    generate_whatsapp()
    
    print("\n" + "=" * 70)
    print("✅ ALL TEMPLATES CREATED")
    print("=" * 70)
    print("\n📁 Location: pending_approval/")
    print("\n📝 NEXT STEPS:")
    print("1. Open the files you want to use")
    print("2. Edit with your content")
    print("3. Save the files")
    print("4. Move to /approved/ when ready")
    print("5. Orchestrator will auto-post (except LinkedIn/WhatsApp)")
    print("\n" + "=" * 70 + "\n")


def show_help():
    """Show help message"""
    print("\n" + "=" * 70)
    print("  AI EMPLOYEE POST GENERATOR")
    print("=" * 70)
    print("""
Usage: python3 scripts/generate_post.py <platform>

Platforms:
  email       - Generate email template
  facebook    - Generate Facebook post template
  instagram   - Generate Instagram post template
  linkedin    - Generate LinkedIn post template
  whatsapp    - Generate WhatsApp message template
  all         - Generate all templates at once

Examples:
  python3 scripts/generate_post.py facebook
  python3 scripts/generate_post.py email
  python3 scripts/generate_post.py all

Workflow:
  1. Generate template
  2. Edit with your content
  3. Save the file
  4. Move to /approved/
  5. Auto-posts (or run manual command for LinkedIn/WhatsApp)
""")
    print("=" * 70 + "\n")


def main():
    if len(sys.argv) < 2:
        show_help()
        return
    
    platform = sys.argv[1].lower()
    
    generators = {
        'email': generate_email,
        'facebook': generate_facebook,
        'fb': generate_facebook,
        'instagram': generate_instagram,
        'ig': generate_instagram,
        'linkedin': generate_linkedin,
        'li': generate_linkedin,
        'whatsapp': generate_whatsapp,
        'wa': generate_whatsapp,
        'all': generate_all,
    }
    
    if platform in generators:
        generators[platform]()
    else:
        print(f"❌ Unknown platform: {platform}")
        show_help()


if __name__ == "__main__":
    main()
