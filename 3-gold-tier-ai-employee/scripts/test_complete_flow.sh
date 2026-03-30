#!/bin/bash
# Complete End-to-End Test Script
# Edits all templates with real content and tests execution

echo "======================================================================"
echo "  AI EMPLOYEE - COMPLETE END-TO-END TEST"
echo "======================================================================"
echo ""

cd /mnt/e/hackathon-0-ai-employee/gold-tier-ai-employee

# Get the latest template files
EMAIL_FILE=$(ls -t pending_approval/EMAIL_POST_*.md 2>/dev/null | head -1)
FACEBOOK_FILE=$(ls -t pending_approval/FACEBOOK_POST_*.md 2>/dev/null | head -1)
INSTAGRAM_FILE=$(ls -t pending_approval/INSTAGRAM_POST_*.md 2>/dev/null | head -1)
LINKEDIN_FILE=$(ls -t pending_approval/LINKEDIN_POST_*.md 2>/dev/null | head -1)

echo "📁 Found templates:"
echo "   Email: $EMAIL_FILE"
echo "   Facebook: $FACEBOOK_FILE"
echo "   Instagram: $INSTAGRAM_FILE"
echo "   LinkedIn: $LINKEDIN_FILE"
echo ""

# Edit Email
echo "✏️  Editing Email template..."
cat > "$EMAIL_FILE" << 'EOF'
---
type: approval_request
action: email_send
to: mwaleedkhan726@gmail.com
subject: AI Employee - End-to-End Production Test
created: 2026-03-25T00:20:00
status: pending
priority: medium
---

# Email - End-to-End Test

## Email Content

Hello,

This is a comprehensive end-to-end test of the AI Employee Gold Tier system.

Test Details:
✅ Template generated via scripts/generate_post.py
✅ Content edited with real message
✅ Approved by moving to /approved/
✅ Auto-executed by orchestrator

System Status: All platforms operational!

Best regards,
AI Employee Gold Tier

---

## Status
Ready to send via orchestrator
EOF
echo "   ✅ Email edited"

# Edit Facebook
echo "✏️  Editing Facebook template..."
cat > "$FACEBOOK_FILE" << 'EOF'
---
type: approval_request
action: facebook_post
platform: facebook
created: 2026-03-25T00:20:00
status: pending
priority: medium
---

# Facebook Post - End-to-End Test

## Post Content

🚀 AI Employee Gold Tier - End-to-End Test!

Our autonomous AI employee system is fully operational and production-ready!

✅ Email automation (Gmail API)
✅ Facebook posting (Meta Graph API)
✅ Instagram posting (Meta Graph API)
✅ LinkedIn posting (Playwright)
✅ WhatsApp messaging (Playwright)
✅ Human-in-the-loop workflow
✅ Comprehensive audit logging

The future of work is here! 🤖

#AI #Automation #GoldTier #ProductionReady #EndToEndTest

---

## Status
Ready to post via orchestrator
EOF
echo "   ✅ Facebook edited"

# Edit Instagram
echo "✏️  Editing Instagram template..."
cat > "$INSTAGRAM_FILE" << 'EOF'
---
type: approval_request
action: instagram_post
platform: instagram
image_url: https://images.unsplash.com/photo-1677442136019-21780ecad995?w=1080&h=1080&fit=crop
created: 2026-03-25T00:20:00
status: pending
priority: medium
---

# Instagram Post - End-to-End Test

## Caption

🤖 AI Employee Gold Tier - Live Test!

Autonomous AI employee system in action!

✅ Multi-platform automation
✅ Real-time monitoring
✅ Smart coordination
✅ Production ready

#AI #Automation #Tech #GoldTier #EndToEndTest #Innovation

---

## Status
Ready to post via orchestrator
EOF
echo "   ✅ Instagram edited"

# Edit LinkedIn
echo "✏️  Editing LinkedIn template..."
cat > "$LINKEDIN_FILE" << 'EOF'
---
type: approval_request
action: linkedin_post
platform: linkedin
created: 2026-03-25T00:20:00
status: pending
priority: medium
---

# LinkedIn Post - End-to-End Test

## Post Content

🎯 Exciting Milestone: AI Employee Gold Tier Complete!

I'm thrilled to announce that our autonomous AI employee system is now fully operational and production-ready!

Key achievements:
✅ Multi-platform integration (Email, Social Media, Messaging)
✅ Human-in-the-loop approval workflow
✅ Real-time monitoring and automation
✅ Comprehensive audit logging
✅ Production-tested and verified

This Gold Tier system handles:
• Gmail, Facebook, Instagram, LinkedIn, WhatsApp
• Automated CEO briefings
• Weekly business audits
• Smart task coordination

The future of autonomous work is here! 🚀

#AI #Automation #Innovation #GoldTier #Productivity #Business #Technology

---

## Status
Ready to post via post_linkedin.py
EOF
echo "   ✅ LinkedIn edited"

echo ""
echo "======================================================================"
echo "  STEP 1 COMPLETE: All templates edited with real content"
echo "======================================================================"
echo ""

# Move all to approved
echo "📁 Moving all to /approved/..."
mv "$EMAIL_FILE" approved/
mv "$FACEBOOK_FILE" approved/
mv "$INSTAGRAM_FILE" approved/
mv "$LINKEDIN_FILE" approved/
echo "   ✅ All files moved to /approved/"
echo ""

echo "======================================================================"
echo "  STEP 2 COMPLETE: All posts approved"
echo "======================================================================"
echo ""

# List what's in approved
echo "📋 Files ready for execution:"
ls -la approved/*.md | grep -E "(EMAIL|FACEBOOK|INSTAGRAM|LINKEDIN)_POST_"
echo ""

echo "======================================================================"
echo "  NEXT STEPS:"
echo "======================================================================"
echo ""
echo "1. Run orchestrator (auto-executes Email, FB, IG):"
echo "   python3 orchestrator.py"
echo ""
echo "2. Run LinkedIn poster (manual):"
echo "   python3 post_linkedin.py"
echo ""
echo "3. Check results:"
echo "   - Email: Check Gmail inbox"
echo "   - Facebook: https://www.facebook.com/1001224683078250"
echo "   - Instagram: Check your profile"
echo "   - LinkedIn: https://www.linkedin.com/feed/"
echo ""
echo "======================================================================"
echo "  READY FOR EXECUTION!"
echo "======================================================================"
