# 🤖 AI Employee - Autonomous Digital FTE (Full-Time Equivalent)

**Your life and business on autopilot. Local-first, agent-driven, human-in-the-loop.**

[![Platinum Tier](https://img.shields.io/badge/Tier-Platinum-orange)](https://github.com)
[![Python 3.12+](https://img.shields.io/badge/Python-3.12+-blue)](https://python.org)
[![Deploy](https://img.shields.io/badge/Deploy-Railway-0B0D0E)](https://railway.app)
[![Status](https://img.shields.io/badge/Status-Production%20Ready-success)](https://github.com)
[![License](https://img.shields.io/badge/License-MIT-yellow)](https://github.com)

---

## 📋 TABLE OF CONTENTS

- [Overview](#-overview)
- [Tier System](#-tier-system)
- [Architecture](#-architecture)
- [Quick Start](#-quick-start)
- [Documentation](#-documentation)
- [Contributing](#-contributing)
- [License](#-license)

---

## 🎯 OVERVIEW

The **AI Employee** is a comprehensive autonomous AI system that manages your personal and business communications 24/7. Built with a local-first, privacy-focused architecture, it uses AI agents to proactively handle emails, social media posts, and messaging while keeping humans in control through an approval workflow.

This project follows a **tiered achievement system** from Bronze to Platinum, allowing you to build and deploy at your own pace.

### **Key Value Proposition:**

| Metric | Human Employee | AI Employee (Platinum) |
|--------|----------------|------------------------|
| Availability | 40 hours/week | **168 hours/week (24/7)** |
| Monthly Cost | $4,000 - $8,000+ | **$10 - $50** (Cloud + API) |
| Response Time | Variable | **<10 seconds** (Cloud) |
| Consistency | 85-95% | **99%+** |
| Scaling | Linear | **Exponential** |

---

## 🏆 TIER SYSTEM

### **🥉 Bronze Tier - Foundation**

**Location:** `1-bronze-tier-ai-employee/`

**Features:**
- Obsidian vault with Dashboard.md
- Company Handbook
- One working Watcher script
- Basic folder structure (/inbox, /needs_action, /done)
- Claude Code integration

**Time:** 8-12 hours

[View Bronze Tier →](1-bronze-tier-ai-employee/)

---

### **🥈 Silver Tier - Functional Assistant**

**Location:** `2-silver-tier-ai-employee/`

**Features:**
- All Bronze features +
- Multiple Watcher scripts (Gmail, WhatsApp)
- LinkedIn auto-posting
- Claude reasoning loop (Plan.md files)
- MCP server for external actions
- Human-in-the-loop approval workflow
- Basic scheduling

**Time:** 20-30 hours

[View Silver Tier →](2-silver-tier-ai-employee/)

---

### **🥇 Gold Tier - Autonomous Employee**

**Location:** `3-gold-tier-ai-employee/`

**Features:**
- All Silver features +
- Full cross-domain integration (Personal + Business)
- Facebook & Instagram integration (Meta Graph API)
- Multiple MCP servers
- Weekly Business Audit + CEO Briefing
- Error recovery & graceful degradation
- Comprehensive audit logging (90-day retention)
- Ralph Wiggum persistence loop

**Time:** 40+ hours

[View Gold Tier →](3-gold-tier-ai-employee/)

---

### **💎 Platinum Tier - Cloud-Native Executive**

**Location:** `4-platinum-tier-ai-employee/`

**Features:**
- All Gold features +
- **24/7 Cloud Deployment** (Railway)
- **Work-Zone Specialization** (Cloud drafts, Local executes)
- **Git-Based Vault Sync** (secure synchronization)
- **Security Isolation** (secrets never sync)
- **A2A Communication** (agent-to-agent via signals)
- Cloud-Local hybrid architecture

**Time:** 60+ hours

[View Platinum Tier →](4-platinum-tier-ai-employee/)

---

## 🏗️ ARCHITECTURE

### **Platinum Tier (Cloud-Native)**

```
┌─────────────────────────────────────────────────────────────────┐
│                    RAILWAY CLOUD VM (24/7)                      │
│  ┌───────────────────────────────────────────────────────────┐ │
│  │  CLOUD AGENT (Draft-Only Domain)                          │ │
│  │  ├── Email Triage → drafts replies (no send)              │ │
│  │  ├── Social Media → draft posts (no publish)              │ │
│  │  └── Cloud Watchers (Gmail, Facebook, Instagram APIs)     │ │
│  └───────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
                              ↕ Git Sync
┌─────────────────────────────────────────────────────────────────┐
│                    LOCAL MACHINE (User Present)                 │
│  ┌───────────────────────────────────────────────────────────┐ │
│  │  LOCAL AGENT (Full Domain + Approvals)                    │ │
│  │  ├── Approvals (HITL workflow)                            │ │
│  │  ├── WhatsApp Session (browser automation)                │ │
│  │  ├── Payments/Banking (secure operations)                 │ │
│  │  └── Final Send/Post Actions                              │ │
│  └───────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
```

### **Workflow**

```
Cloud detects → Creates draft → Writes to /Updates/ → Pushes to Git
    ↓
Local pulls → Merges to /needs_action/ → Creates approval
    ↓
Human approves (drag-drop) → Local executes → Moves to /Done/
    ↓
Local pushes to Git → Cloud sees audit trail
```

---

## 🚀 QUICK START

### **Start with Bronze Tier**

```bash
cd 1-bronze-tier-ai-employee
pip install -r requirements.txt
python3 main.py
```

### **Deploy Platinum Tier**

```bash
cd 4-platinum-tier-ai-employee

# Install dependencies
pip install -r requirements.txt
playwright install chromium

# Deploy to Railway
railway login
railway init
railway up

# Start Local Agent
python3 main.py
```

See individual tier README files for detailed instructions.

---

## 📚 DOCUMENTATION

### **Core Documentation**

- **[ai-employee.md](ai-employee.md)** - Complete architectural blueprint and hackathon guide
- **[README.md](README.md)** - This file (project overview)

### **Tier Documentation**

| Tier | README | Guide | Requirements |
|------|--------|-------|--------------|
| Bronze | [README](1-bronze-tier-ai-employee/README.md) | - | [Tests](1-bronze-tier-ai-employee/test_bronze_tier.py) |
| Silver | [README](2-silver-tier-ai-employee/README.md) | [PRODUCTION_GUIDE](2-silver-tier-ai-employee/PRODUCTION_GUIDE.md) | - |
| Gold | [README](3-gold-tier-ai-employee/README.md) | [SYSTEM_GUIDE](3-gold-tier-ai-employee/SYSTEM_GUIDE.md) | [Analysis](3-gold-tier-ai-employee/REQUIREMENTS_ANALYSIS.md) |
| Platinum | [README](4-platinum-tier-ai-employee/README.md) | [PLATINUM_GUIDE](4-platinum-tier-ai-employee/PLATINUM_GUIDE.md) | [Analysis](4-platinum-tier-ai-employee/REQUIREMENTS_ANALYSIS.md) |

### **Learning Resources**

- **Claude Code Fundamentals** - [Documentation](https://agentfactory.panaversity.org/docs/AI-Tool-Landscape/claude-code-features-and-workflows)
- **Obsidian Setup** - [help.obsidian.md](https://help.obsidian.md/Getting+started)
- **MCP Protocol** - [modelcontextprotocol.io](https://modelcontextprotocol.io/introduction)
- **Agent Skills** - [Claude Documentation](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview)

---

## 🏗️ PROJECT STRUCTURE

```
hackathon-0-/
├── 📘 ai-employee.md              # Master blueprint
├── 📘 README.md                    # This file
│
├── 🥉 1-bronze-tier-ai-employee/   # Foundation
│   ├── main.py
│   ├── polling_watcher.py
│   ├── dashboard.md
│   └── company_handbook.md
│
├── 🥈 2-silver-tier-ai-employee/   # Functional Assistant
│   ├── main.py
│   ├── orchestrator.py
│   ├── scheduler.py
│   ├── watchers/
│   ├── skills/
│   └── mcp_servers/
│
├── 🥇 3-gold-tier-ai-employee/     # Autonomous Employee
│   ├── main.py
│   ├── orchestrator.py
│   ├── scheduler.py
│   ├── watchers/
│   ├── skills/
│   ├── mcp_servers/
│   └── scripts/
│
└── 💎 4-platinum-tier-ai-employee/ # Cloud-Native Executive
    ├── cloud_agent.py              # Cloud entry point
    ├── main.py                     # Local entry point
    ├── cloud/                      # Cloud-specific code
    ├── local/                      # Local-specific code
    ├── sync/                       # Vault sync system
    ├── scripts/                    # Sync utilities
    ├── railway.json                # Railway deployment
    └── nixpacks.toml               # Build configuration
```

---

## 🤝 CONTRIBUTING

1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

### **Development Workflow**

1. Start with Bronze Tier to understand fundamentals
2. Progress through tiers sequentially
3. Test each tier thoroughly before advancing
4. Document all changes in tier README files

---

## 📄 LICENSE

This project is licensed under the MIT License - see the LICENSE file for details.

---

## 📧 SUPPORT

- **Documentation:** See tier-specific guides
- **Issues:** GitHub Issues
- **Community:** Panaversity Discord

---

## 🏆 ACKNOWLEDGMENTS

- **Hackathon:** Personal AI Employee Hackathon 0
- **Community:** Panaversity
- **Tools:** Claude Code, Obsidian, Playwright, Meta Graph API, Railway

---

**Built with ❤️ for the future of autonomous AI employees**

*From Bronze to Platinum - Your AI Employee Journey*
