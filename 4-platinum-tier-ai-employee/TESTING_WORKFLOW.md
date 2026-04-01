# 🎬 GOLD TIER - COMPLETE TESTING WORKFLOW

**For Recording Demo Video**  
**Date:** March 25, 2026  
**Status:** ✅ Ready for Testing

---

## 📋 PRE-TEST CHECKLIST

### 1. Verify System is Clean
```bash
cd /mnt/e/hackathon-0-ai-employee/gold-tier-ai-employee

# Check folders are empty
ls -la done/ approved/ pending_approval/ needs_action/ plans/
# Should show no .md files
```

### 2. Verify Credentials
```bash
# Check .env exists and has credentials
cat .env | grep -E "(GMAIL|FACEBOOK|INSTAGRAM)" | head -10

# Should show:
# GMAIL_CLIENT_ID=...
# GMAIL_REFRESH_TOKEN=...
# FACEBOOK_PAGE_ID=...
# FACEBOOK_PAGE_ACCESS_TOKEN=...
# INSTAGRAM_BUSINESS_ACCOUNT_ID=...
# INSTAGRAM_ACCESS_TOKEN=...
```

### 3. Verify All Files Exist
```bash
# Core system files
ls -la main.py orchestrator.py scheduler.py post_linkedin.py

# Scripts folder
ls -la scripts/generate_post.py

# Skills folder
ls -la skills/whatsapp_sender.py skills/linkedin_poster_final.py

# MCP servers
ls -la mcp_servers/email_mcp.py mcp_servers/facebook_mcp_api.py mcp_servers/instagram_mcp_api.py

# Watchers
ls -la watchers/gmail_watcher.py watchers/whatsapp_watcher.py watchers/facebook_watcher.py watchers/instagram_watcher.py watchers/linkedin_watcher.py
```

---

## 🎬 TESTING WORKFLOW (RECORD THIS)

### **SCENE 1: Introduction (30 seconds)**

**Show on Screen:** Terminal at `gold-tier-ai-employee/` folder

**Say:**
> "This is my Gold Tier AI Employee - a production-ready autonomous AI system that manages communications across 5 platforms: Email, Facebook, Instagram, LinkedIn, and WhatsApp."

**Command to Show:**
```bash
pwd
ls -la
```

---

### **SCENE 2: System Overview (1 minute)**

**Show on Screen:** SYSTEM_GUIDE.md

**Say:**
> "The system uses Human-in-the-Loop workflow. All actions require approval before execution. Let me show you how it works."

**Command to Show:**
```bash
cat SYSTEM_GUIDE.md | head -50
```

---

### **SCENE 3: Generate Test Templates (2 minutes)**

**Show on Screen:** Running the post generator

**Say:**
> "First, I'll generate editable templates for all platforms. These templates are created in the pending_approval folder with clear instructions."

**Commands:**
```bash
# Generate all templates at once
python3 scripts/generate_post.py all

# Show created files
ls -la pending_approval/
```

**Expected Output:**
```
✅ Email template created: EMAIL_POST_20260325_HHMMSS.md
✅ Facebook template created: FACEBOOK_POST_20260325_HHMMSS.md
✅ Instagram template created: INSTAGRAM_POST_20260325_HHMMSS.md
✅ LinkedIn template created: LINKEDIN_POST_20260325_HHMMSS.md
✅ WhatsApp template created: WHATSAPP_MESSAGE_20260325_HHMMSS.md
```

---

### **SCENE 4: Edit Email Template (2 minutes)**

**Show on Screen:** Editing email template with nano

**Say:**
> "Now I'll edit each template with real content. Let me start with email - I need to add recipient, subject, and message."

**Commands:**
```bash
# Open email template
nano pending_approval/EMAIL_POST_*.md
```

**Edit to Look Like:**
```markdown
---
type: approval_request
action: email_send
to: mwaleedkhan726@gmail.com
subject: AI Employee Gold Tier - Live Test
created: 2026-03-25T12:00:00
status: pending
---

# Email - Live Test

## Email Content

Hello,

This is a live test of the AI Employee Gold Tier system.

Test Details:
✅ Template generated via scripts/generate_post.py
✅ Content edited manually
✅ Approved by moving to approved/
✅ Auto-executed by orchestrator

System Status: All platforms operational!

Best regards,
AI Employee Gold Tier
```

**Save and Exit:** Ctrl+O, Enter, Ctrl+X

---

### **SCENE 5: Edit Facebook Template (2 minutes)**

**Show on Screen:** Editing Facebook template

**Say:**
> "For Facebook, I'll write a professional post about the AI Employee system."

**Commands:**
```bash
nano pending_approval/FACEBOOK_POST_*.md
```

**Edit to Look Like:**
```markdown
---
type: approval_request
action: facebook_post
platform: facebook
created: 2026-03-25T12:00:00
status: pending
---

# Facebook Post - Live Test

## Post Content

🚀 AI Employee Gold Tier - Live Production Test!

Our autonomous AI employee system is fully operational and ready for real-world use.

✅ Email automation (Gmail API)
✅ Facebook posting (Meta Graph API)
✅ Instagram posting (Meta Graph API)
✅ LinkedIn posting (Playwright)
✅ WhatsApp messaging (Playwright)
✅ Human-in-the-loop workflow

#AI #Automation #GoldTier #ProductionReady
```

---

### **SCENE 6: Edit Instagram Template (2 minutes)**

**Show on Screen:** Editing Instagram template

**Say:**
> "Instagram requires an image URL and caption. I'll use a tech-themed image from Unsplash."

**Commands:**
```bash
nano pending_approval/INSTAGRAM_POST_*.md
```

**Edit to Look Like:**
```markdown
---
type: approval_request
action: instagram_post
platform: instagram
image_url: https://images.unsplash.com/photo-1677442136019-21780ecad995?w=1080&h=1080&fit=crop
created: 2026-03-25T12:00:00
status: pending
---

# Instagram Post - Live Test

## Caption

🤖 AI Employee Gold Tier - Live Test!

Autonomous AI employee system in action!

✅ Multi-platform automation
✅ Real-time monitoring
✅ Smart coordination
✅ Production ready

#AI #Automation #Tech #GoldTier #Innovation
```

---

### **SCENE 7: Approve All Templates (1 minute)**

**Show on Screen:** Moving files to approved folder

**Say:**
> "Now I'll approve all templates by moving them to the approved folder. The orchestrator will automatically detect and execute them within 10 seconds."

**Commands:**
```bash
# Move all to approved
mv pending_approval/EMAIL_POST_*.md approved/
mv pending_approval/FACEBOOK_POST_*.md approved/
mv pending_approval/INSTAGRAM_POST_*.md approved/

# Show approved files
ls -la approved/
```

---

### **SCENE 8: Watch Orchestrator Execute (3 minutes)**

**Show on Screen:** Running orchestrator and watching execution

**Say:**
> "The orchestrator runs every 10 seconds, checking for approved files. Let me run it manually to show the execution."

**Commands:**
```bash
# Run orchestrator for 30 seconds
timeout 30 python3 orchestrator.py 2>&1 | grep -E "(Executing|sent|successful|Error)"
```

**Expected Output:**
```
2026-03-25 12:05:00 - Orchestrator - INFO - Executing approved action: EMAIL_POST_*.md
2026-03-25 12:05:01 - Orchestrator - INFO - ✓ Email sent to mwaleedkhan726@gmail.com
2026-03-25 12:05:02 - Orchestrator - INFO - Executing approved action: FACEBOOK_POST_*.md
2026-03-25 12:05:06 - Orchestrator - INFO - ✓ Facebook post successful: 1001224683078250_...
2026-03-25 12:05:07 - Orchestrator - INFO - Executing approved action: INSTAGRAM_POST_*.md
2026-03-25 12:05:17 - Orchestrator - INFO - ✓ Instagram post successful: 18085655170990265
```

---

### **SCENE 9: Verify Execution (2 minutes)**

**Show on Screen:** Checking done folder and platforms

**Say:**
> "Let me verify that all files were executed and moved to the done folder. Then I'll check each platform to confirm the posts are live."

**Commands:**
```bash
# Check done folder
ls -la done/

# Should show:
# EMAIL_POST_*.md
# FACEBOOK_POST_*.md
# INSTAGRAM_POST_*.md
```

**Show Browser Tabs:**
1. Gmail Inbox: Check for test email
2. Facebook Page: https://www.facebook.com/1001224683078250
3. Instagram Profile: Check for new post

---

### **SCENE 10: LinkedIn Test (3 minutes)**

**Show on Screen:** LinkedIn template and execution

**Say:**
> "LinkedIn uses browser automation, so it requires manual execution. Let me show you how it works."

**Commands:**
```bash
# Show LinkedIn template
cat approved/LINKEDIN_POST_*.md | head -30

# Run LinkedIn poster
python3 post_linkedin.py
```

**Expected Output:**
```
📄 File: LINKEDIN_POST_*.md
📝 Content: AI Employee Gold Tier announcement

[1/7] Opening browser...
[2/7] Going to LinkedIn feed...
[3/7] Clicking 'Start a post'...
[4/7] Entering content...
[5/7] Waiting for Post button...
[6/7] Posting...
[7/7] Complete!

✅ LINKEDIN POST SUCCESSFUL!
📱 Check: https://www.linkedin.com/feed/
```

---

### **SCENE 11: WhatsApp Test (3 minutes)**

**Show on Screen:** WhatsApp template and execution

**Say:**
> "WhatsApp also uses browser automation with saved session. Let me test it with a simple message."

**Commands:**
```bash
# Show WhatsApp template
cat approved/WHATSAPP_MESSAGE_*.md

# Run WhatsApp sender
python3 skills/whatsapp_sender.py
```

**Expected Output:**
```
💬 WHATSAPP SENDER - SESSION VERSION

📱 Found 1 message(s)

📱 To: 03352121689
💬 Message: Hello! This is a test message...

[1/10] Starting Playwright...
[2/10] Launching browser with saved session...
[3/10] Waiting for WhatsApp Web to load...
...
[8/10] Sending message...
    ✓ Send button clicked!
[9/10] Waiting for delivery confirmation...
    ✓ Delivered! (5s)

✅ MESSAGE SENT & DELIVERED!
```

---

### **SCENE 12: System Status (1 minute)**

**Show on Screen:** Dashboard and logs

**Say:**
> "Finally, let me show you the system status and audit logs. Every action is logged for complete transparency."

**Commands:**
```bash
# Check system status
cat dashboard.md | head -50

# Check audit logs
ls -la logs/audit/

# Check recent logs
tail -50 logs/orchestrator_*.log
```

---

### **SCENE 13: Conclusion (1 minute)**

**Show on Screen:** Terminal with summary

**Say:**
> "This completes the Gold Tier AI Employee testing workflow. All 5 platforms are working:
> - ✅ Email sent via Gmail API
> - ✅ Facebook posted via Meta Graph API
> - ✅ Instagram posted via Meta Graph API
> - ✅ LinkedIn posted via Playwright
> - ✅ WhatsApp sent via Playwright with session
> 
> The system is production-ready and uses Human-in-the-Loop workflow for safety."

**Final Commands:**
```bash
# Show final status
echo "=== GOLD TIER TEST COMPLETE ==="
echo ""
echo "Files Executed:"
ls -la done/*.md | wc -l
echo ""
echo "System Status: PRODUCTION READY ✅"
```

---

## 🎯 QUICK COMMAND REFERENCE

### Full Test Sequence (Copy-Paste Friendly):

```bash
# 1. Setup
cd /mnt/e/hackathon-0-ai-employee/gold-tier-ai-employee
ls -la

# 2. Generate templates
python3 scripts/generate_post.py all
 timeout 30 python3 orchestrator.py
# 3. Edit templates (use nano)
nano pending_approval/EMAIL_POST_*.md
nano pending_approval/FACEBOOK_POST_*.md
nano pending_approval/INSTAGRAM_POST_*.md

# 4. Approve
mv pending_approval/EMAIL_POST_*.md approved/
mv pending_approval/FACEBOOK_POST_*.md approved/
mv pending_approval/INSTAGRAM_POST_*.md approved/

# 5. Run orchestrator
timeout 30 python3 orchestrator.py 2>&1 | grep -E "(Executing|sent|successful)"

# 6. Verify
ls -la done/

# 7. LinkedIn (manual)
python3 post_linkedin.py

# 8. WhatsApp (manual)
python3 skills/whatsapp_sender.py

# 9. Check logs
tail -50 logs/orchestrator_*.log

# 10. Final status
echo "=== TEST COMPLETE ==="
```

---

## ⏱️ TIMING BREAKDOWN

| Scene | Duration | What to Show |
|-------|----------|--------------|
| 1. Introduction | 30s | Terminal, folder structure |
| 2. System Overview | 1m | SYSTEM_GUIDE.md |
| 3. Generate Templates | 2m | `python3 scripts/generate_post.py all` |
| 4. Edit Email | 2m | nano editor |
| 5. Edit Facebook | 2m | nano editor |
| 6. Edit Instagram | 2m | nano editor |
| 7. Approve | 1m | mv commands |
| 8. Orchestrator | 3m | Execution output |
| 9. Verify | 2m | Browser tabs, done folder |
| 10. LinkedIn | 3m | Browser automation |
| 11. WhatsApp | 3m | Browser automation |
| 12. System Status | 1m | Dashboard, logs |
| 13. Conclusion | 1m | Summary |

**Total: ~26 minutes**

---

## 🎬 RECORDING TIPS

1. **Use OBS Studio** for screen recording
2. **Increase font size** in terminal for better visibility
3. **Use dark theme** for better contrast
4. **Pause between commands** to let output show
5. **Highlight key output** with mouse or cursor
6. **Show browser tabs** for platform verification
7. **Keep terminal clean** - clear between major sections

---

## ✅ SUCCESS CRITERIA

Your recording is complete when:
- [ ] All 5 platforms tested
- [ ] Email received in Gmail
- [ ] Facebook post visible on page
- [ ] Instagram post visible on profile
- [ ] LinkedIn post visible on feed
- [ ] WhatsApp message delivered
- [ ] All files in /done/ folder
- [ ] Audit logs created
- [ ] Clear explanation of HITL workflow

---

**Good luck with your recording! 🎬**

*Gold Tier AI Employee - Testing Workflow Guide*
