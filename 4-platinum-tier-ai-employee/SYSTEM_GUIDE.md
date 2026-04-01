# 🚀 AI EMPLOYEE GOLD TIER - COMPLETE SYSTEM GUIDE

**Production-Ready Autonomous AI Employee**  
**Last Updated:** March 25, 2026  
**Status:** ✅ 100% Operational - All 5 Platforms Working

---

## 📋 TABLE OF CONTENTS

1. [Quick Start](#quick-start)
2. [System Overview](#system-overview)
3. [Platform Commands](#platform-commands)
4. [Complete Workflow](#complete-workflow)
5. [Folder Structure](#folder-structure)
6. [Configuration](#configuration)
7. [Troubleshooting](#troubleshooting)

---

## ⚡ QUICK START

### Post to Any Platform (3 Steps):

```bash
# 1. Generate editable template
python3 scripts/generate_post.py facebook

# 2. Edit with your content
nano pending_approval/FACEBOOK_POST_*.md

# 3. Approve (auto-posts in 10 seconds)
mv pending_approval/FACEBOOK_POST_*.md approved/
```

### Test All Platforms:
```bash
python3 test_posts.py all
```

---

## 🎯 SYSTEM OVERVIEW

### What It Does:
Your AI Employee autonomously manages communications across 5 platforms:

| Platform | Method | Auto-Execute | Speed |
|----------|--------|--------------|-------|
| **Email** | Gmail API | ✅ Yes | <10 seconds |
| **Facebook** | Meta Graph API | ✅ Yes | ~4 seconds |
| **Instagram** | Meta Graph API | ✅ Yes | ~10 seconds |
| **LinkedIn** | Playwright | ⚠️ Manual | 60-90 seconds |
| **WhatsApp** | Playwright + Session | ✅ Yes | ~3 minutes |

### Architecture:
```
WATCHERS (Perception)
  ↓
NEEDS_ACTION
  ↓
ORCHESTRATOR (Brain)
  ↓
PENDING_APPROVAL → Human Review → APPROVED
  ↓
AUTO-EXECUTE (Email, FB, IG, WA) or MANUAL (LinkedIn)
  ↓
DONE (Audit Trail)
```

---

## 📱 PLATFORM COMMANDS

### Email (Gmail API)
```bash
# Generate template
python3 scripts/generate_post.py email

# Edit content (add recipient, subject, body)
nano pending_approval/EMAIL_POST_*.md

# Approve (auto-sends in 10 seconds)
mv pending_approval/EMAIL_POST_*.md approved/
```

### Facebook (Meta Graph API)
```bash
# Generate template
python3 scripts/generate_post.py facebook

# Edit content (write post)
nano pending_approval/FACEBOOK_POST_*.md

# Approve (auto-posts in ~4 seconds)
mv pending_approval/FACEBOOK_POST_*.md approved/
```

### Instagram (Meta Graph API)
```bash
# Generate template
python3 scripts/generate_post.py instagram

# Edit content (add image URL + caption)
nano pending_approval/INSTAGRAM_POST_*.md

# Approve (auto-posts in ~10 seconds)
mv pending_approval/INSTAGRAM_POST_*.md approved/
```

### LinkedIn (Playwright - Manual)
```bash
# Generate template
python3 scripts/generate_post.py linkedin

# Edit content (write professional post)
nano pending_approval/LINKEDIN_POST_*.md

# Approve
mv pending_approval/LINKEDIN_POST_*.md approved/

# Post manually (browser opens)
python3 post_linkedin.py
```

### WhatsApp (Playwright + Session)
```bash
# Generate template
python3 scripts/generate_post.py whatsapp

# Edit content (add phone + message)
nano pending_approval/WHATSAPP_MESSAGE_*.md

# Approve & Send (session-based, ~3 minutes)
mv pending_approval/WHATSAPP_MESSAGE_*.md approved/
python3 skills/whatsapp_sender.py
```

---

## 🔄 COMPLETE WORKFLOW

### Step-by-Step Process:

```
1. GENERATE TEMPLATE
   python3 scripts/generate_post.py facebook
   ↓
   Creates: pending_approval/FACEBOOK_POST_YYYYMMDD_HHMMSS.md

2. EDIT CONTENT
   nano pending_approval/FACEBOOK_POST_*.md
   ↓
   Replace [bracketed placeholders] with real content

3. APPROVE
   mv pending_approval/FACEBOOK_POST_*.md approved/
   ↓
   File is now in approval queue

4. AUTO-EXECUTE (10 seconds)
   Orchestrator detects file in /approved/
   Executes via appropriate MCP server
   ↓
   Post is live on platform!

5. AUDIT TRAIL
   File automatically moved to /done/
   Logs created in /logs/audit/
```

### Real-World Example:

```bash
# Post product launch on Facebook
python3 scripts/generate_post.py facebook

# Edit with:
# 🚀 Introducing Our New AI Product!
# Learn more: https://yourcompany.com
# #AI #ProductLaunch

mv pending_approval/FACEBOOK_POST_*.md approved/

# Check Facebook page in 10 seconds!
```

---

## 📁 FOLDER STRUCTURE

```
gold-tier-ai-employee/
├── 📂 pending_approval/     ← Edit templates here
├── 📂 approved/             ← Move when ready to post
├── 📂 done/                 ← Executed files (audit trail)
├── 📂 needs_action/         ← Watchers create files here
├── 📂 plans/                ← Processing plans
├── 📂 logs/                 ← System logs
│   └── audit/              ← Structured audit logs
├── 📂 scripts/              ← Post generators
│   └── generate_post.py    ← Main generator (all 5 platforms)
├── 📂 watchers/             ← Platform monitors
├── 📂 mcp_servers/          ← Action servers
├── 📂 skills/               ← Agent skills
│   ├── whatsapp_sender.py  ← WhatsApp automation
│   └── linkedin_poster_final.py ← LinkedIn automation
├── 📄 main.py               ← Start autonomous system
├── 📄 orchestrator.py       ← Task coordinator
├── 📄 scheduler.py          ← Scheduled operations
├── 📄 post_linkedin.py      ← LinkedIn quick post
├── 📄 test_posts.py         ← Quick test (no editing)
├── 📄 .env                  ← Configuration (DO NOT COMMIT)
├── 📘 README.md             ← This file
├── 📘 business_goals.md     ← Your business objectives
├── 📘 company_handbook.md   ← Rules & guidelines
└── 📘 dashboard.md          ← System status
```

---

## ⚙️ CONFIGURATION

### Environment Variables (.env):

```bash
# System
DEMO_MODE=false
AUDIT_RETENTION_DAYS=90

# Gmail API
GMAIL_CLIENT_ID=your_client_id
GMAIL_CLIENT_SECRET=your_secret
GMAIL_REFRESH_TOKEN=your_token
GMAIL_DEMO_MODE=false

# Meta API (Facebook & Instagram)
META_APP_ID=your_app_id
META_APP_SECRET=your_secret
FACEBOOK_PAGE_ID=your_page_id
FACEBOOK_PAGE_ACCESS_TOKEN=your_token
INSTAGRAM_BUSINESS_ACCOUNT_ID=your_account_id
INSTAGRAM_ACCESS_TOKEN=your_token
FACEBOOK_DEMO_MODE=false
INSTAGRAM_DEMO_MODE=false

# WhatsApp
WHATSAPP_ENABLED=true
WHATSAPP_KEYWORDS=urgent,asap,invoice,payment,help
```

### Start Autonomous System:
```bash
python3 main.py
```

This runs:
- All watchers (Gmail, WhatsApp, FB, IG, LinkedIn)
- Orchestrator (auto-executes approved files)
- Scheduler (daily briefings, weekly audits)

---

## 🔧 TROUBLESHOOTING

### Email Not Sending:
```bash
# Check credentials
cat .env | grep GMAIL

# Regenerate token if needed
python3 -c "from google.oauth2.credentials import Credentials; print('Check credentials')"

# Test manually
python3 -c "from mcp_servers.email_mcp import EmailMCPServer; s=EmailMCPServer(); print(s.demo_mode)"
```

### Facebook/Instagram Not Posting:
```bash
# Check Meta API credentials
cat .env | grep -E "(FACEBOOK|INSTAGRAM|META)"

# Verify page access token doesn't expire
# Regenerate if needed from Meta Developers
```

### WhatsApp Not Sending:
```bash
# Check session exists
ls -la sessions/whatsapp/

# Run with debug
python3 skills/whatsapp_sender_fixed.py

# Check screenshots in logs/
ls -la logs/wa_*.png
```

### LinkedIn Not Posting:
```bash
# Ensure display/X11 available
# Browser must open for Playwright

# Run manually
python3 post_linkedin.py

# Or with specific file
python3 skills/linkedin_poster_final.py --file approved/LINKEDIN_*.md
```

### Orchestrator Not Executing:
```bash
# Check orchestrator running
ps aux | grep orchestrator

# Run manually
timeout 30 python3 orchestrator.py 2>&1 | grep -E "(Executing|approved|done)"

# Check logs
tail -50 logs/orchestrator_*.log
```

### General Issues:
```bash
# Check Python dependencies
pip3 list | grep -E "(google|playwright|meta)"

# Reinstall if needed
pip3 install -r requirements.txt

# Check file permissions
ls -la pending_approval/ approved/ done/

# Verify folder structure
find . -maxdepth 2 -type d | sort
```

---

## 📊 MONITORING & AUDIT

### Check System Status:
```bash
# Pending approvals
ls -la pending_approval/

# Recently executed
ls -lt done/ | head -10

# System logs
tail -100 logs/orchestrator_*.log

# Audit trail
ls -la logs/audit/
```

### Daily Workflow:
```bash
# Morning: Check overnight activity
ls -la needs_action/
ls -la pending_approval/

# Review and approve
cat pending_approval/*.md
mv pending_approval/APPROVED_FILE.md approved/

# Evening: Check what was posted
ls -la done/ | grep $(date +%Y%m%d)
```

---

## 🎯 BEST PRACTICES

### 1. Content Templates:
Create templates for common posts:
```bash
mkdir templates
# Save reusable templates for:
# - Product announcements
# - Email responses
# - Weekly updates
```

### 2. File Naming:
Use descriptive names:
```
FACEBOOK_PRODUCT_LAUNCH_20260325.md
EMAIL_CLIENT_ABC_RESPONSE.md
LINKEDIN_CASE_STUDY_XYZ.md
```

### 3. Review Before Approving:
Always check content in `pending_approval/` before moving to `approved/`

### 4. Monitor Logs:
```bash
# Check execution status
tail -f logs/orchestrator_*.log

# Check audit trail
cat logs/audit/*.jsonl | head -20
```

### 5. Regular Cleanup:
```bash
# Archive old done files (monthly)
mkdir -p archive/2026-03
mv done/*.md archive/2026-03/

# Clean old logs (keep 90 days)
find logs/ -name "*.log" -mtime +90 -delete
```

---

## 🎉 QUICK REFERENCE

### All Commands:
```bash
# Generate templates
python3 scripts/generate_post.py email
python3 scripts/generate_post.py facebook
python3 scripts/generate_post.py instagram
python3 scripts/generate_post.py linkedin
python3 scripts/generate_post.py whatsapp
python3 scripts/generate_post.py all

# Quick tests (no editing)
python3 test_posts.py email
python3 test_posts.py facebook
python3 test_posts.py instagram
python3 test_posts.py linkedin

# Post to LinkedIn
python3 post_linkedin.py

# Send WhatsApp
python3 skills/whatsapp_sender.py

# Start autonomous system
python3 main.py
```

### Platform Summary:
| Platform | Generate | Auto-Post | Manual Command |
|----------|----------|-----------|----------------|
| Email | `generate_post.py email` | ✅ Yes | - |
| Facebook | `generate_post.py facebook` | ✅ Yes | - |
| Instagram | `generate_post.py instagram` | ✅ Yes | - |
| LinkedIn | `generate_post.py linkedin` | ⚠️ No | `post_linkedin.py` |
| WhatsApp | `generate_post.py whatsapp` | ✅ Yes | `whatsapp_sender.py` |

---

## 📖 ADDITIONAL DOCUMENTATION

- `business_goals.md` - Your business objectives and KPIs
- `company_handbook.md` - Rules and guidelines for AI behavior
- `dashboard.md` - System status and metrics
- `README.md` - Original project documentation

---

**Gold Tier AI Employee - Production System**  
**Generated:** March 25, 2026  
**Status:** ✅ 100% Operational  
**Platforms:** 5/5 Working
