# 🥇 Gold Tier AI Employee - Autonomous Digital FTE

**Your life and business on autopilot. Local-first, agent-driven, human-in-the-loop.**

[![Gold Tier](https://img.shields.io/badge/Tier-Gold-brightgreen)](https://github.com)
[![Python 3.12+](https://img.shields.io/badge/Python-3.12+-blue)](https://python.org)
[![Status](https://img.shields.io/badge/Status-Production%20Ready-success)](https://github.com)
[![License](https://img.shields.io/badge/License-MIT-yellow)](https://github.com)

---

## 🎬 DEMO VIDEO

**Watch the Gold Tier AI Employee in action:** [**▶️ YouTube Demo**](https://youtu.be/Sl1o89oTldM)

---

## 🎯 OVERVIEW

The **Gold Tier AI Employee** is a production-ready autonomous AI system that manages your personal and business communications across **5 platforms** 24/7. Built with a local-first, privacy-focused architecture, it uses AI agents to proactively handle emails, social media posts, and messaging while keeping humans in control through an approval workflow.

### **Key Value Proposition**

| Metric | Human Employee | AI Employee |
|--------|----------------|-------------|
| Availability | 40 hours/week | **168 hours/week (24/7)** |
| Monthly Cost | $4,000 - $8,000+ | **$50 - $200** (API costs) |
| Response Time | Variable | **<10 seconds** (API-based) |
| Consistency | 85-95% | **99%+** |
| Scaling | Linear | **Exponential** |

---

## ✨ KEY ACHIEVEMENTS

### **🌐 Multi-Platform Automation**

- ✅ **Gmail** - Send/receive emails via Gmail API
- ✅ **Facebook** - Post updates via Meta Graph API
- ✅ **Instagram** - Post photos via Meta Graph API
- ✅ **LinkedIn** - Professional posts via browser automation
- ✅ **WhatsApp** - Messaging via browser automation

### **🔒 Human-in-the-Loop (HITL)**

- All sensitive actions require approval
- Drag-and-drop approval workflow (VS Code friendly)
- Automatic status updates when files moved
- No unauthorized actions

### **📊 Business Intelligence**

- CEO Briefing Generator (weekly audits)
- Task completion tracking
- Communication metrics
- Bottleneck identification
- Proactive suggestions

### **🛡️ Production-Ready Features**

- Comprehensive audit logging (90-day retention)
- Error recovery & graceful degradation
- Session management for browser automation
- Demo mode for testing without credentials
- Tamper-evident audit trails

---

## 🏗️ ARCHITECTURE

```
┌─────────────────────────────────────────────────────────┐
│                    AI EMPLOYEE                          │
├─────────────────────────────────────────────────────────┤
│  PERCEPTION LAYER (Watchers)                            │
│  ├── Gmail Watcher (API)                                │
│  ├── WhatsApp Watcher (Playwright)                      │
│  ├── Facebook Watcher (API)                             │
│  ├── Instagram Watcher (API)                            │
│  └── LinkedIn Watcher (Playwright)                      │
├─────────────────────────────────────────────────────────┤
│  REASONING LAYER (Brain)                                │
│  ├── Orchestrator (task coordination)                   │
│  ├── Scheduler (daily/weekly tasks)                     │
│  └── Ralph Wiggum (persistence loop)                    │
├─────────────────────────────────────────────────────────┤
│  ACTION LAYER (MCP Servers + Skills)                    │
│  ├── Email MCP (Gmail API)                              │
│  ├── Facebook MCP (Meta Graph API)                      │
│  ├── Instagram MCP (Meta Graph API)                     │
│  ├── LinkedIn Poster (Playwright)                       │
│  └── WhatsApp Sender (Playwright)                       │
└─────────────────────────────────────────────────────────┘
```

### **Workflow**

```
Watcher detects → /needs_action/ → Orchestrator creates Plan.md
    ↓
Approval needed? → /pending_approval/ → Human approves (drag-drop)
    ↓
/orchestrator auto-executes (API) or manual (Playwright)
    ↓
/done/ (audit trail)
```

---

## 📁 PROJECT STRUCTURE

```
3-gold-tier-ai-employee/
├── 📂 watchers/             # Perception layer (5 platforms)
│   ├── gmail_watcher.py
│   ├── whatsapp_watcher.py
│   ├── facebook_watcher.py
│   ├── instagram_watcher.py
│   └── linkedin_watcher.py
├── 📂 mcp_servers/          # Action layer (API integrations)
│   ├── email_mcp.py
│   ├── facebook_mcp_api.py
│   └── instagram_mcp_api.py
├── 📂 skills/               # Agent skills (modular)
│   ├── approval_workflow.py
│   ├── audit_logger.py
│   ├── ceo_briefing_generator.py
│   ├── linkedin_poster_final.py
│   ├── whatsapp_sender.py
│   └── social_media_poster.py
├── 📂 scripts/              # Utility scripts
│   └── generate_post.py    # Post template generator
├── 📂 pending_approval/     # Awaiting human review
├── 📂 approved/             # Ready to execute
├── 📂 done/                 # Executed (audit trail)
├── 📄 main.py               # Main entry point
├── 📄 orchestrator.py       # Task coordinator
├── 📄 scheduler.py          # Scheduled operations
├── 📄 ralph_wiggum.py       # Persistence loop
├── 📘 SYSTEM_GUIDE.md       # Complete system guide
└── 📘 REQUIREMENTS_ANALYSIS.md  # Tier compliance report
```

---

## ✅ IMPLEMENTATION STATUS

### **Gold Tier Requirements: 10/10 (100%)**

| Requirement | Status | Implementation |
|-------------|--------|----------------|
| All Silver Tier | ✅ | Complete |
| Cross-domain integration | ✅ | Personal + Business |
| Facebook & Instagram | ✅ | Meta Graph API |
| Multiple MCP servers | ✅ | Email, Facebook, Instagram |
| Weekly Audit + CEO Briefing | ✅ | Auto-generated |
| Error recovery | ✅ | Graceful degradation |
| Audit logging | ✅ | 90-day retention |
| Ralph Wiggum loop | ✅ | Implemented |
| Documentation | ✅ | Complete |
| Agent Skills | ✅ | All modularized |

**Optional (Excluded per user request):**
- ⚠️ Odoo accounting integration
- ⚠️ Twitter/X integration

**Status: ✅ GOLD TIER ACHIEVED**

---

## 🚀 QUICK START

### **Prerequisites**

```bash
# Python 3.12+
python3 --version

# Install dependencies
pip install -r requirements.txt

# Install Playwright browsers
playwright install chromium
```

### **Configuration**

```bash
# Copy environment template
cp .env.example .env

# Edit with your credentials:
# - Gmail API (OAuth2)
# - Meta API (Facebook & Instagram)
# - LinkedIn (browser automation)
```

### **Run the System**

```bash
# Start autonomous system
python3 main.py

# Or run components individually:
python3 orchestrator.py    # Task coordination
python3 scheduler.py       # Scheduled operations
python3 post_linkedin.py   # Quick LinkedIn post
```

---

## 🔒 HUMAN-IN-THE-LOOP WORKFLOW

### **Approval Process**

1. **Template Created** → `pending_approval/FILE.md`
2. **User Reviews** → Edit content if needed
3. **User Approves** → Move to `approved/` folder
4. **System Executes** → Auto-executes (API) or manual (Playwright)
5. **Audit Trail** → File moved to `done/`

### **Execution Methods**

| Platform | Method | Auto-Execute |
|----------|--------|--------------|
| Email | Gmail API | ✅ Yes |
| Facebook | Meta Graph API | ✅ Yes |
| Instagram | Meta Graph API | ✅ Yes |
| LinkedIn | Playwright | ⚠️ Manual |
| WhatsApp | Playwright | ⚠️ Manual |

---

## 📊 DEMO VIDEO HIGHLIGHTS

The [YouTube demo](https://youtu.be/Sl1o89oTldM) showcases:

1. **System Architecture** - Overview of Gold Tier components
2. **Multi-Platform Integration** - Gmail, Facebook, Instagram, LinkedIn, WhatsApp
3. **HITL Workflow** - Drag-and-drop approval process
4. **Auto-Execution** - API-based platforms execute automatically
5. **Audit Logging** - Complete audit trail in `/done/` folder
6. **CEO Briefing** - Weekly business audit generation

---

## 🧪 TESTING

### **Quick Test**

```bash
# Generate test posts for all platforms
python3 scripts/generate_post.py all

# Review generated templates
ls pending_approval/

# Approve all
mv pending_approval/*.md approved/

# Execute (wait for orchestrator)
timeout 30 python3 orchestrator.py

# Verify completion
ls done/
```

### **Platform-Specific Tests**

```bash
# Email test
python3 scripts/generate_post.py email
# Edit → Approve → Auto-sends in 10s

# Facebook test
python3 scripts/generate_post.py facebook
# Edit → Approve → Auto-posts in 4s

# Instagram test
python3 scripts/generate_post.py instagram
# Edit → Approve → Auto-posts in 10s
```

---

## 📖 DOCUMENTATION

- **[SYSTEM_GUIDE.md](SYSTEM_GUIDE.md)** - Complete system guide with setup instructions
- **[REQUIREMENTS_ANALYSIS.md](REQUIREMENTS_ANALYSIS.md)** - Gold Tier compliance report
- **[TESTING_WORKFLOW.md](TESTING_WORKFLOW.md)** - Testing guide

---

## 🤝 CONTRIBUTING

1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

---

## 📄 LICENSE

This project is licensed under the MIT License.

---

## 🏆 ACKNOWLEDGMENTS

- **Hackathon:** Personal AI Employee Hackathon 0
- **Community:** Panaversity
- **Tools:** Claude Code, Obsidian, Playwright, Meta Graph API

---

**Built with ❤️ for the future of autonomous AI employees**

*Gold Tier AI Employee v1.0 - Production Ready*
