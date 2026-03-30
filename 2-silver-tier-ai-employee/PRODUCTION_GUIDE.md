# 🚀 SILVER TIER AI EMPLOYEE - PRODUCTION GUIDE

## ✅ PRODUCTION READY SYSTEM

**Three fully automated communication channels:**
- 📧 **Gmail** - Real email sending via Gmail API
- 💬 **WhatsApp** - WhatsApp Web automation
- 📱 **LinkedIn** - LinkedIn posting automation

**All with Human-in-the-Loop (HITL) approval workflow!**

---

## 📁 FOLDER STRUCTURE

```
silver-tier-ai-employee/
├── watchers/              # Monitoring services
│   ├── gmail_watcher.py   # Monitors Gmail inbox
│   ├── whatsapp_watcher.py # Monitors WhatsApp Web
│   └── linkedin_watcher.py # Monitors post requests
│
├── skills/                # Action services
│   ├── whatsapp_sender.py # Sends WhatsApp messages
│   ├── linkedin_poster_final.py # Posts to LinkedIn
│   └── [other skills...]
│
├── mcp_servers/
│   └── email_mcp.py       # Sends emails via Gmail API
│
├── needs_action/          # Auto-detected items
├── pending_approval/      # Awaiting your review
├── approved/              # Ready to execute
├── done/                  # Completed items
└── logs/                  # Audit trail
```

---

## 🎯 COMPLETE WORKFLOW

```
┌─────────────────┐
│ 1. WATCHER      │
│ Detects item    │
│ Creates file    │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ 2. PENDING      │
│ pending_approval/│
│ You review here │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ 3. APPROVE      │
│ Move to:        │
│ approved/       │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ 4. EXECUTE      │
│ Run sender      │
│ Automatic!      │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ 5. DONE         │
│ Moved to:       │
│ done/           │
└─────────────────┘
```

---

## 📧 GMAIL AUTOMATION

### **What It Does:**
- Monitors your Gmail inbox every 2 minutes
- Detects new emails automatically
- Creates action files for each email
- Sends replies via Gmail API (requires approval)

### **Setup (One-Time):**
Already configured with your OAuth credentials!

### **Daily Workflow:**

```bash
# 1. Start Gmail Watcher
cd /mnt/e/hackathon-0-ai-employee/silver-tier-ai-employee
source venv/bin/activate
python watchers/gmail_watcher.py &

# 2. Check detected emails
ls needs_action/EMAIL_*.md

# 3. Review emails
cat needs_action/EMAIL_*.md

# 4. Check for approval requests
ls pending_approval/

# 5. Review and approve
cat pending_approval/APPROVAL_*.md
mv pending_approval/APPROVAL_*.md approved/

# 6. Send emails (automatic!)
python -m mcp_servers.email_mcp

# 7. Verify sent
ls done/
```

### **Real Example:**

```bash
# Client emails: "Can you send me the invoice?"

# Watcher detects → Creates: needs_action/EMAIL_*.md
# You review → Move to: approved/
# Email MCP sends → Moves to: done/
# Check Gmail Sent folder - email is there!
```

---

## 💬 WHATSAPP AUTOMATION

### **What It Does:**
- Monitors WhatsApp Web 24/7
- Detects messages with keywords: `urgent`, `asap`, `invoice`, `payment`, `help`, `meeting`, `deadline`
- Creates action files automatically
- Sends replies via WhatsApp Web (requires approval)

### **Setup (One-Time):**

```bash
# First time authentication
cd /mnt/e/hackathon-0-ai-employee/silver-tier-ai-employee
source venv/bin/activate
python watchers/whatsapp_watcher.py

# Browser opens → Scan QR code with phone
# WhatsApp Web loads → Scroll through chats
# Ctrl+C when done
# Session saved for 30 days
```

### **Daily Workflow:**

```bash
# 1. Start WhatsApp Watcher
python watchers/whatsapp_watcher.py &

# 2. Check detected messages
ls needs_action/WHATSAPP_*.md

# 3. Review messages
cat needs_action/WHATSAPP_*.md

# 4. Create reply approval
# Edit file in pending_approval/ with reply_message:

# 5. Approve
mv pending_approval/WHATSAPP_REPLY_*.md approved/

# 6. Send (automatic!)
python -m skills.whatsapp_sender

# 7. Verify
ls done/
# Check your phone - message sent!
```

### **Real Example:**

```bash
# Client sends WhatsApp: "urgent: Need invoice ASAP"

# Watcher detects "urgent" → Creates: needs_action/WHATSAPP_*.md
# You add reply → Move to: approved/
# WhatsApp sender sends → Moves to: done/
# Check WhatsApp - message delivered!
```

---

## 📱 LINKEDIN AUTOMATION

### **What It Does:**
- Monitors for LinkedIn post requests
- Creates approval files with generated content
- Posts to your LinkedIn profile automatically (requires approval)

### **Setup (One-Time):**

```bash
# First time authentication
cd /mnt/e/hackathon-0-ai-employee/silver-tier-ai-employee
source venv/bin/activate
python watchers/linkedin_watcher.py

# Browser opens → Log in to LinkedIn
# Wait for feed to load → Scroll briefly
# Ctrl+C when done
# Session saved for 30 days
```

### **Daily Workflow:**

```bash
# 1. Create post request
nano needs_action/LINKEDIN_POST.md
```

**Content format:**
```markdown
---
type: linkedin_post_request
topic: Your Topic
---

## Post Content
```
Your LinkedIn post text here...
#Hashtags #Here
```
```

```bash
# 2. Run watcher to create approval
python watchers/linkedin_watcher.py &

# 3. Review approval
cat pending_approval/LINKEDIN_POST_*.md

# 4. Approve and post
mv pending_approval/LINKEDIN_POST_*.md approved/
python -m skills.linkedin_poster_final

# 5. Verify
ls done/
# Check LinkedIn - post is live!
```

### **Real Example:**

```bash
# Create business update post
cat > needs_action/LINKEDIN_POST.md << 'EOF'
---
type: linkedin_post_request
topic: Business Update
---

## Post Content
```
🎉 Exciting news! We launched our new AI automation service.

Contact us to learn more!

#AI #Automation #Business
```
EOF

# Run watcher, approve, and post!
```

---

## 📋 MONITORING & MANAGEMENT

### **Start All Watchers:**

```bash
cd /mnt/e/hackathon-0-ai-employee/silver-tier-ai-employee
source venv/bin/activate

# Start all in background
python watchers/gmail_watcher.py &
python watchers/whatsapp_watcher.py &
python watchers/linkedin_watcher.py &

echo "✅ All watchers running!"
```

### **Check System Status:**

```bash
# What's waiting for action?
ls needs_action/
ls pending_approval/

# What's been completed?
ls done/

# Check logs
tail -f logs/*_watcher_*.log
```

### **Stop All Watchers:**

```bash
pkill -f gmail_watcher
pkill -f whatsapp_watcher
pkill -f linkedin_watcher
```

---

## 🔧 TROUBLESHOOTING

### **Gmail Issues:**

| Problem | Solution |
|---------|----------|
| **Not authenticated** | Check .env has GMAIL_REFRESH_TOKEN |
| **Email not sent** | Check approved/ folder and run email_mcp |
| **API error** | Check logs/gmail_watcher_*.log |

### **WhatsApp Issues:**

| Problem | Solution |
|---------|----------|
| **Not logged in** | Run `python watchers/whatsapp_watcher.py` and scan QR |
| **Message not sent** | Check session in sessions/whatsapp/ |
| **Number not found** | Verify number format and has WhatsApp |

### **LinkedIn Issues:**

| Problem | Solution |
|---------|----------|
| **Not logged in** | Run `python watchers/linkedin_watcher.py` and log in |
| **Post not published** | Check browser stays open during posting |
| **Session expired** | Re-authenticate with watcher |

---

## ✅ PRODUCTION CHECKLIST

### **Daily:**
- [ ] Start all watchers (morning)
- [ ] Check `needs_action/` (twice daily)
- [ ] Review `pending_approval/` (twice daily)
- [ ] Approve and execute items

### **Weekly:**
- [ ] Check logs for errors
- [ ] Review completed items in `done/`
- [ ] Verify sessions still active

### **Monthly:**
- [ ] Archive old `done/` files
- [ ] Re-authenticate LinkedIn if needed
- [ ] Re-authenticate WhatsApp if needed (30 days)
- [ ] Review and update keywords

---

## 📞 QUICK COMMAND REFERENCE

| Action | Command |
|--------|---------|
| **Start Gmail** | `python watchers/gmail_watcher.py &` |
| **Start WhatsApp** | `python watchers/whatsapp_watcher.py &` |
| **Start LinkedIn** | `python watchers/linkedin_watcher.py &` |
| **Check Pending** | `ls pending_approval/` |
| **Approve All** | `mv pending_approval/*.md approved/` |
| **Send WhatsApp** | `python -m skills.whatsapp_sender` |
| **Send Email** | `python -m mcp_servers.email_mcp` |
| **Post LinkedIn** | `python -m skills.linkedin_poster_final` |
| **Stop All** | `pkill -f watcher` |
| **View Logs** | `tail -f logs/*_watcher_*.log` |

---

## 🎉 YOU'RE READY!

**The system is production-ready. Just:**

1. Start watchers
2. Let them monitor
3. Review approvals
4. Approve and execute

**That's it! The AI Employee handles the rest!** 🚀

---

**Last Updated:** 2026-03-17  
**Status:** ✅ Production Ready  
**Tested:** ✅ All 3 channels verified working
