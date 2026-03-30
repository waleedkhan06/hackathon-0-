# Gold Tier Quick Start Guide

**Last Updated**: March 21, 2026

---

## 🚀 Quick Start (5 Minutes)

### Step 1: Install Dependencies (2 min)
```bash
cd gold-tier-ai-employee
pip install -r requirements.txt
playwright install chromium
```

### Step 2: Configure Environment (1 min)
```bash
cp .env.example .env
# Keep demo mode enabled for testing
```

### Step 3: Run the System (2 min)
```bash
python main.py
```

That's it! The system is now running in demo mode.

---

## 📊 What Happens in Demo Mode?

- ✅ All watchers run and generate demo data
- ✅ No real API calls made
- ✅ No real posts published
- ✅ Safe to test all features
- ✅ See how the system works

---

## 🔧 Enable Real Integrations

### Twitter (API-based)

**1. Get API Keys:**
- Go to https://developer.twitter.com/
- Create app and apply for Elevated Access
- Generate API keys

**2. Configure `.env`:**
```bash
TWITTER_API_KEY=your_api_key_here
TWITTER_API_SECRET=your_api_secret_here
TWITTER_ACCESS_TOKEN=your_access_token_here
TWITTER_ACCESS_TOKEN_SECRET=your_access_token_secret_here
TWITTER_BEARER_TOKEN=your_bearer_token_here
TWITTER_DEMO_MODE=false
```

**3. Restart system**

---

### Facebook (Playwright - No API Keys!)

**1. Configure `.env`:**
```bash
FACEBOOK_DEMO_MODE=false
```

**2. Run system:**
```bash
python main.py
```

**3. Browser will open automatically:**
- Log in to Facebook manually
- Session is saved in `/sessions/facebook/`
- Future runs use saved session (no login needed)

**4. Done!** Facebook integration is now active.

---

### Instagram (Playwright - No API Keys!)

**1. Configure `.env`:**
```bash
INSTAGRAM_DEMO_MODE=false
```

**2. Run system:**
```bash
python main.py
```

**3. Browser will open automatically:**
- Log in to Instagram manually
- Session is saved in `/sessions/instagram/`
- Future runs use saved session (no login needed)

**4. Done!** Instagram integration is now active.

---

## 📁 Important Folders

### Where to Look

| Folder | What's There | Check Frequency |
|--------|--------------|-----------------|
| `/pending_approval` | **⭐ REVIEW HERE** - Posts awaiting approval | Daily |
| `/briefings` | CEO briefings (every Monday) | Weekly |
| `/summaries` | Social media performance reports | Weekly |
| `/inbox` | Drop files here to process | As needed |
| `/needs_action` | Tasks requiring AI processing | Daily |
| `/done` | Completed tasks archive | Monthly |
| `/logs` | System logs and screenshots | When debugging |

### How to Approve Posts

1. Go to `/pending_approval` folder
2. Open the approval file (e.g., `APPROVAL_Twitter_Post_20260321.md`)
3. Review the content
4. **To Approve**: Move file to `/approved` folder
5. **To Reject**: Move file to `/rejected` folder

---

## 📅 Scheduled Operations

### What Happens Automatically

**Every Day:**
- 08:00 - Morning briefing generated
- 18:00 - End of day summary

**Every Week:**
- Sunday 23:00 - Business audit runs
- Monday 07:00 - CEO briefing generated and emailed

**Social Media Posts:**
- Monday 10:00 - Twitter
- Tuesday 14:00 - Facebook
- Wednesday 10:00 - Twitter
- Wednesday 15:00 - Instagram
- Thursday 14:00 - Facebook
- Friday 10:00 - Twitter
- Friday 15:00 - Instagram

---

## 🔍 Monitoring the System

### Check System Status

**Option 1: Dashboard**
```bash
cat dashboard.md
```

**Option 2: Verification Script**
```bash
python3 verify_setup.py
```

**Option 3: Logs**
```bash
# View today's logs
ls -lh logs/

# View specific watcher
tail -f logs/twitter_watcher_20260321.log
```

---

## 🐛 Troubleshooting

### "Playwright not installed"
```bash
pip install playwright
playwright install chromium
```

### "Twitter API 401 Error"
- Check API keys in `.env` are correct
- Verify you have Elevated Access
- Check keys haven't expired

### "Facebook/Instagram session expired"
```bash
# Delete old session
rm -rf sessions/facebook/
# or
rm -rf sessions/instagram/

# Run system again - browser will open for re-login
python main.py
```

### "No CEO briefing generated"
- Check `SCHEDULER_ENABLED=true` in `.env`
- Verify it's Monday morning
- Check `/logs/ceo_briefing_*.log` for errors

### "Posts not appearing in pending_approval"
- Check watchers are running (see logs)
- Verify demo mode is disabled for that platform
- Check `/logs/social_media_manager_*.log`

---

## 💡 Pro Tips

### 1. Test in Demo Mode First
Always test new configurations in demo mode before enabling real integrations.

### 2. Check Pending Approvals Daily
Set a reminder to check `/pending_approval` folder every morning.

### 3. Review CEO Briefings
Every Monday, check `/briefings` for the weekly business summary.

### 4. Monitor Logs
If something seems off, check the logs in `/logs` folder.

### 5. Backup Sessions
The `/sessions` folder contains your login sessions. Back it up to avoid re-logging in.

### 6. Use Screenshots
When posts are published, screenshots are saved in `/logs` for verification.

---

## 📚 Documentation

- `README.md` - Full system documentation
- `API_SETUP_GUIDE.md` - Detailed API setup instructions
- `IMPLEMENTATION_SUMMARY.md` - Technical implementation details
- `FINAL_SUMMARY.md` - Complete project summary
- `PLAYWRIGHT_CONVERSION_COMPLETE.md` - Playwright implementation details
- `company_handbook.md` - System rules and guidelines
- `business_goals.md` - Business objectives and KPIs

---

## 🎯 Common Tasks

### Add a New Task
```bash
# Option 1: Drop a file in inbox
cp task.txt inbox/

# Option 2: Create directly in needs_action
echo "# New Task\n\nTask description here" > needs_action/task_$(date +%Y%m%d).md
```

### Post to Social Media
1. Create post content
2. System generates approval request
3. Review in `/pending_approval`
4. Move to `/approved` to publish

### Check Social Media Performance
```bash
# View latest summary
ls -lt summaries/ | head -1
cat summaries/Social_Media_Summary_*.md
```

### Review Business Performance
```bash
# View latest CEO briefing
ls -lt briefings/ | head -1
cat briefings/CEO_Briefing_*.md
```

---

## 🔐 Security Best Practices

1. **Never commit `.env` file** - Contains sensitive credentials
2. **Rotate API keys monthly** - Especially Twitter keys
3. **Backup sessions securely** - Contains authentication cookies
4. **Review all approvals** - Don't auto-approve sensitive actions
5. **Monitor audit logs** - Check `/logs/audit/` regularly
6. **Use strong passwords** - For Facebook/Instagram accounts
7. **Enable 2FA** - On all social media accounts

---

## 📞 Getting Help

### Check These First
1. Verification script: `python3 verify_setup.py`
2. System logs: `ls -lh logs/`
3. Dashboard: `cat dashboard.md`
4. Documentation: `README.md`

### Common Questions

**Q: Do I need API keys for Facebook/Instagram?**
A: No! They use Playwright browser automation. Just login once.

**Q: How often do I need to login to Facebook/Instagram?**
A: Usually once. Sessions persist for weeks/months.

**Q: Can I use personal accounts?**
A: Yes! Playwright works with personal accounts (unlike APIs).

**Q: Is Twitter API free?**
A: Yes, but you need to apply for Elevated Access.

**Q: How do I stop the system?**
A: Press Ctrl+C in the terminal.

---

## 🎉 You're Ready!

The Gold Tier AI Employee system is now set up and ready to use. Start with demo mode, then enable real integrations one at a time.

**Happy automating!** 🚀

---

*Gold Tier Quick Start Guide v1.0*
*Last Updated: March 21, 2026*
