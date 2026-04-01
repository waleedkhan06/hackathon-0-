# 📘 PLATINUM TIER AI EMPLOYEE - COMPLETE GUIDE

**Cloud-Native Autonomous Digital FTE**
**Version:** 1.0
**Last Updated:** April 2026

---

## 📋 TABLE OF CONTENTS

1. [Introduction](#introduction)
2. [Architecture Overview](#architecture-overview)
3. [Cloud vs Local Domains](#cloud-vs-local-domains)
4. [Deployment Guide](#deployment-guide)
5. [Vault Sync System](#vault-sync-system)
6. [Human-in-the-Loop Workflow](#human-in-the-loop-workflow)
7. [Security Architecture](#security-architecture)
8. [Monitoring & Health](#monitoring--health)
9. [Troubleshooting](#troubleshooting)
10. [API Reference](#api-reference)

---

## INTRODUCTION

### What is Platinum Tier?

Platinum Tier is a **cloud-native, production-grade autonomous AI system** with hybrid Cloud-Local architecture. It extends Gold Tier with:

- ✅ **24/7 Always-On Cloud Deployment** (Railway)
- ✅ **Work-Zone Specialization** (Cloud drafts, Local executes)
- ✅ **Git-Based Vault Sync** (secure synchronization)
- ✅ **Security Isolation** (secrets never sync)
- ✅ **A2A Communication** (agent-to-agent via signals)

### Key Differences from Gold Tier

| Feature | Gold Tier | Platinum Tier |
|---------|-----------|---------------|
| Deployment | Local only | Cloud + Local hybrid |
| Availability | When machine on | 24/7 always-on |
| Email Response | Local dependent | Cloud drafts immediately |
| WhatsApp | Local only | Local only (session isolated) |
| Banking | Local only | Local only (credentials isolated) |
| Sync | None | Git-based vault sync |

### Use Cases

1. **Business Email Management**
   - Cloud drafts replies 24/7
   - Local reviews and sends during work hours

2. **Social Media Automation**
   - Cloud creates post drafts continuously
   - Local approves and publishes

3. **Customer Support**
   - Cloud triages incoming messages
   - Local handles sensitive responses

4. **E-commerce Operations**
   - Cloud monitors orders, drafts responses
   - Local processes payments, ships orders

---

## ARCHITECTURE OVERVIEW

### System Components

```
┌─────────────────────────────────────────────────────────┐
│              RAILWAY CLOUD (24/7 Always-On)             │
│  ┌───────────────────────────────────────────────────┐ │
│  │  Cloud Agent (Draft-Only Domain)                  │ │
│  │  ├── Cloud Orchestrator                           │ │
│  │  ├── Cloud Watchers (Gmail, FB, IG APIs)          │ │
│  │  └── Vault Sync (push drafts)                     │ │
│  └───────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────┘
                        ↕ Git Sync
┌─────────────────────────────────────────────────────────┐
│              LOCAL MACHINE (User Present)               │
│  ┌───────────────────────────────────────────────────┐ │
│  │  Local Agent (Full Domain + Approvals)            │ │
│  │  ├── Local Orchestrator                           │ │
│  │  ├── All Watchers (including WhatsApp, LinkedIn)  │ │
│  │  ├── HITL Approval Workflow                       │ │
│  │  ├── Vault Sync (pull drafts, push completions)   │ │
│  │  └── Dashboard.md (single writer)                 │ │
│  └───────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────┘
```

### Data Flow

1. **Cloud Detects Email** → Creates draft → Writes to `/Updates/`
2. **Cloud Pushes** → Git repository
3. **Local Pulls** → Git repository → Merges from `/Updates/`
4. **Local Creates Approval** → User reviews
5. **User Approves** → Local executes send
6. **Local Pushes** → `/Done/` → Cloud sees audit trail

---

## CLOUD VS LOCAL DOMAINS

### Cloud Agent (Draft-Only)

**Can Do:**
- ✅ Monitor Gmail API 24/7
- ✅ Monitor Facebook API
- ✅ Monitor Instagram API
- ✅ Draft email replies
- ✅ Draft social media posts
- ✅ Write to `/Updates/` folder
- ✅ Push to Git

**Cannot Do:**
- ❌ Send emails (no send token)
- ❌ Publish social posts (no publish token)
- ❌ Access WhatsApp (no browser session)
- ❌ Access banking (no credentials)
- ❌ Write Dashboard.md (Local only)

### Local Agent (Full Domain)

**Can Do:**
- ✅ Everything Cloud can do, PLUS:
- ✅ Send emails (has send token)
- ✅ Publish social posts (has publish token)
- ✅ WhatsApp messaging (has browser session)
- ✅ Banking/payments (has credentials)
- ✅ Grant/reject approvals (HITL)
- ✅ Write Dashboard.md (single writer)

**Cannot Do:**
- ❌ Run when machine is off (availability limited)

---

## DEPLOYMENT GUIDE

### Prerequisites

- Python 3.12+
- Git account (GitHub/GitLab/Bitbucket)
- Railway account (for Cloud deployment)
- API credentials (Gmail, Meta)

### Step 1: Clone Repository

```bash
git clone <your-repo-url>
cd 4-platinum-tier-ai-employee
```

### Step 2: Setup Vault Sync

```bash
# Run setup script
python3 scripts/setup_vault_sync.py

# Follow prompts:
# 1. Select deployment mode (Cloud or Local)
# 2. Enter agent name
# 3. Enter Git remote URL
```

### Step 3: Deploy Cloud Agent (Railway)

```bash
# Install Railway CLI
npm install -g @railway/cli

# Login
railway login

# Initialize project
railway init

# Set environment variables
railway variables set \
  DEPLOYMENT_MODE=cloud \
  CLOUD_AGENT_NAME=cloud-primary \
  GMAIL_CLIENT_ID=xxx \
  GMAIL_CLIENT_SECRET=xxx \
  GMAIL_REFRESH_TOKEN=xxx \
  META_APP_ID=xxx \
  META_APP_SECRET=xxx

# Deploy
railway up
```

### Step 4: Configure Local Agent

```bash
# Copy environment template
cp .env.example.local .env.local

# Edit .env.local with your credentials
nano .env.local

# Start Local Agent
python3 main.py
```

### Step 5: Test Sync

```bash
# On Cloud (Railway logs)
railway logs

# On Local (pull updates)
python3 scripts/pull_cloud_updates.py

# Merge Cloud drafts
python3 scripts/merge_cloud_updates.py
```

---

## VAULT SYNC SYSTEM

### Sync Rules

| Rule | Description |
|------|-------------|
| **Single-Writer** | Only Local writes `Dashboard.md` |
| **Claim-by-Move** | First agent to move task owns it |
| **Cloud Writes** | Cloud writes to `/Updates/`, `/Signals/` |
| **Local Merges** | Local merges `/Updates/` to workflow |
| **Secrets Never Sync** | `.env`, tokens, sessions excluded |

### Sync Folders

```
platinum-tier/
├── updates/           # Cloud drafts → Local merges
├── signals/           # A2A communication
├── in_progress/       # Claimed tasks (claim-by-move)
│   ├── cloud-primary/
│   └── local-primary/
├── done/              # Completed tasks (audit trail)
└── dashboard.md       # Local only (single writer)
```

### Manual Sync Commands

```bash
# Cloud: Push drafts
python3 scripts/push_cloud_updates.py

# Local: Pull drafts
python3 scripts/pull_cloud_updates.py

# Local: Merge drafts
python3 scripts/merge_cloud_updates.py

# Local: Push completions
git add done/
git commit -m "Completions"
git push origin main
```

---

## HUMAN-IN-THE-LOOP WORKFLOW

### Approval Flow

```
1. Cloud detects email → drafts reply
2. Cloud writes draft → /Updates/
3. Cloud pushes → Git
4. Local pulls → Git
5. Local merges → /Needs_Action/
6. Local creates approval → /Pending_Approval/
7. User reviews → drags to /Approved/
8. Local executes → sends email
9. Local moves → /Done/
10. Local pushes → Git (Cloud sees audit)
```

### Approval Commands

```bash
# List pending approvals
ls pending_approval/

# Approve (move to approved)
mv pending_approval/APPROVAL_*.md approved/

# Reject (move to rejected)
mv pending_approval/APPROVAL_*.md rejected/

# Execute (automatic when moved to approved)
python3 orchestrator.py
```

---

## SECURITY ARCHITECTURE

### Secrets Isolation

**Never Synced to Git:**
- `.env`, `.env.local`, `.env.cloud`
- `*.token`, `*.session`
- `sessions/`, `secure/`, `credentials/`

**Git Configuration:**
```gitignore
# .gitignore
.env
.env.local
.env.cloud
*.token
*.session
sessions/
```

### Credential Separation

| Credential | Cloud | Local |
|------------|-------|-------|
| Gmail Read | ✅ | ✅ |
| Gmail Send | ❌ | ✅ |
| Facebook Draft | ✅ | ✅ |
| Facebook Publish | ❌ | ✅ |
| WhatsApp Session | ❌ | ✅ |
| Banking Token | ❌ | ✅ |

### Audit Logging

All actions logged to `/logs/audit/`:
- Timestamp
- Action type
- Actor (Cloud/Local)
- Result
- Hash (tamper-evident)

---

## MONITORING & HEALTH

### Railway Dashboard

```bash
# View logs
railway logs

# Check status
railway status

# Open dashboard
railway open
```

### Health Endpoints

Cloud Agent exposes `/health` endpoint:
```json
{
  "status": "healthy",
  "agent": "cloud-primary",
  "uptime": "72h 15m",
  "last_sync": "2026-04-01T10:30:00Z"
}
```

### Local Monitoring

```bash
# Check sync status
python3 -c "from sync.vault_sync import VaultSync; print(VaultSync('.', 'local').get_sync_status())"

# View audit logs
cat logs/audit/audit_*.jsonl | jq
```

---

## TROUBLESHOOTING

### Common Issues

**1. Sync Fails**

```bash
# Check Git status
git status

# Resolve conflicts
git merge --abort
git pull --no-edit -X ours

# Re-run setup
python3 scripts/setup_vault_sync.py
```

**2. Cloud Agent Crashes**

```bash
# View Railway logs
railway logs

# Restart deployment
railway restart

# Check environment variables
railway variables
```

**3. Local Agent Won't Start**

```bash
# Check .env.local
cat .env.local

# Verify credentials
python3 -c "from dotenv import load_dotenv; load_dotenv('.env.local'); print('OK')"

# Check logs
cat logs/local_agent_*.log
```

**4. Drafts Not Syncing**

```bash
# Cloud: Check updates folder
ls updates/

# Local: Pull manually
python3 scripts/pull_cloud_updates.py

# Local: Merge manually
python3 scripts/merge_cloud_updates.py
```

---

## API REFERENCE

### VaultSync Class

```python
from sync.vault_sync import VaultSync

# Initialize
sync = VaultSync(project_path='.', agent_name='local-primary')

# Initialize Git
sync.initialize_git(remote_url='https://github.com/user/repo.git')

# Pull updates
result = sync.pull_updates()

# Push updates
result = sync.push_updates()

# Merge Cloud drafts (Local only)
result = sync.merge_updates()

# Claim task
result = sync.claim_task(task_file=Path('task.md'))

# Release task
result = sync.release_task(task_file=Path('task.md'), destination='done')

# Get sync status
result = sync.get_sync_status()
```

### Cloud Orchestrator

```python
from cloud.cloud_orchestrator import CloudOrchestrator

# Initialize
orchestrator = CloudOrchestrator(project_path='.', agent_name='cloud-primary')

# Check for new tasks
tasks = orchestrator.check_needs_action()

# Create draft
result = orchestrator.create_draft(task_file=Path('task.md'))

# Check completions
completed = orchestrator.check_completed()
```

### Local Orchestrator

```python
from local.local_orchestrator import LocalOrchestrator

# Initialize
orchestrator = LocalOrchestrator(project_path='.', agent_name='local-primary')

# Check for new tasks (includes Cloud drafts)
tasks = orchestrator.check_needs_action()

# Create plan
plan = orchestrator.create_plan(task_file=Path('task.md'))

# Execute approved action
result = orchestrator.execute_approved_action(approval_file=Path('approval.md'))
```

---

## APPENDIX

### A. Railway Environment Variables

```
DEPLOYMENT_MODE=cloud
CLOUD_AGENT_NAME=cloud-primary
GMAIL_CLIENT_ID=xxx
GMAIL_CLIENT_SECRET=xxx
GMAIL_REFRESH_TOKEN=xxx
META_APP_ID=xxx
META_APP_SECRET=xxx
FACEBOOK_PAGE_ID=xxx
FACEBOOK_PAGE_ACCESS_TOKEN=xxx
INSTAGRAM_BUSINESS_ACCOUNT_ID=xxx
INSTAGRAM_ACCESS_TOKEN=xxx
SYNC_INTERVAL_SECONDS=60
```

### B. Local Environment Variables

```
DEPLOYMENT_MODE=local
LOCAL_AGENT_NAME=local-primary
GMAIL_CLIENT_ID=xxx
GMAIL_CLIENT_SECRET=xxx
GMAIL_REFRESH_TOKEN=xxx
GMAIL_SEND_TOKEN=xxx
WHATSAPP_SESSION_PATH=/path/to/session
BANK_API_TOKEN=xxx
PAYMENT_API_KEY=xxx
META_APP_ID=xxx
META_APP_SECRET=xxx
FACEBOOK_PAGE_ACCESS_TOKEN=xxx
INSTAGRAM_ACCESS_TOKEN=xxx
LINKEDIN_EMAIL=xxx
LINKEDIN_PASSWORD=xxx
SYNC_INTERVAL_SECONDS=60
```

### C. Demo Workflow

```bash
# 1. Generate test email
python3 scripts/generate_post.py email

# 2. Cloud detects → drafts → pushes
# (automatic on Cloud Agent)

# 3. Local pulls → merges
python3 scripts/pull_cloud_updates.py
python3 scripts/merge_cloud_updates.py

# 4. User approves
mv pending_approval/*.md approved/

# 5. Local executes
timeout 30 python3 orchestrator.py

# 6. Verify
ls done/
```

---

*Platinum Tier AI Employee - Complete Guide v1.0*
*Built with ❤️ for autonomous AI employees*
