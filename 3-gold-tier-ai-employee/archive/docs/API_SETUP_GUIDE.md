# Gold Tier - API vs Playwright Setup Guide

## Overview

The Gold Tier uses a **hybrid approach** for social media integration:
- **Twitter**: API-based (requires API keys)
- **Facebook**: Playwright browser automation (no API keys)
- **Instagram**: Playwright browser automation (no API keys)

---

## Twitter (API-Based) ✅

### What You Need
Twitter API v2 credentials with **Elevated Access**

### Setup Steps
1. Go to [Twitter Developer Portal](https://developer.twitter.com/)
2. Create a new app
3. Apply for **Elevated Access** (required for posting)
4. Generate credentials:
   - API Key
   - API Secret
   - Access Token
   - Access Token Secret
   - Bearer Token

### Add to `.env`
```bash
TWITTER_API_KEY=your_api_key_here
TWITTER_API_SECRET=your_api_secret_here
TWITTER_ACCESS_TOKEN=your_access_token_here
TWITTER_ACCESS_TOKEN_SECRET=your_access_token_secret_here
TWITTER_BEARER_TOKEN=your_bearer_token_here
TWITTER_DEMO_MODE=false
```

### Features
- ✅ Post tweets
- ✅ Reply to mentions
- ✅ Post threads
- ✅ Like/retweet
- ✅ Monitor mentions
- ✅ Get engagement metrics

---

## Facebook (Playwright-Based) 🎭

### What You Need
- Facebook account
- Browser session (saved by Playwright)

### Setup Steps
1. **No API keys needed!**
2. First run will open browser
3. Log in to Facebook manually
4. Session is saved in `/sessions/facebook/`
5. Future runs use saved session

### How It Works
```python
# Facebook poster uses Playwright
from playwright.sync_api import sync_playwright

# Opens browser with saved session
context = playwright.chromium.launch_persistent_context(
    './sessions/facebook/',
    headless=False
)

# Navigates to Facebook and posts
page.goto('https://www.facebook.com/')
page.click('text=What\'s on your mind')
page.fill('[role="textbox"]', post_content)
page.click('text=Post')
```

### Features
- ✅ Post to timeline/page
- ✅ Upload images
- ✅ Monitor comments
- ✅ Reply to comments
- ⚠️ Requires manual login first time

---

## Instagram (Playwright-Based) 🎭

### What You Need
- Instagram account
- Browser session (saved by Playwright)

### Setup Steps
1. **No API keys needed!**
2. First run will open browser
3. Log in to Instagram manually
4. Session is saved in `/sessions/instagram/`
5. Future runs use saved session

### How It Works
```python
# Instagram poster uses Playwright
from playwright.sync_api import sync_playwright

# Opens browser with saved session
context = playwright.chromium.launch_persistent_context(
    './sessions/instagram/',
    headless=False
)

# Navigates to Instagram and posts
page.goto('https://www.instagram.com/')
page.click('[aria-label="New post"]')
# Upload image and add caption
```

### Features
- ✅ Post photos
- ✅ Add captions
- ✅ Monitor comments
- ✅ Reply to comments
- ⚠️ Requires manual login first time

---

## Comparison

| Platform | Method | API Keys Needed? | First-Time Setup | Automation Level |
|----------|--------|------------------|------------------|------------------|
| **Twitter** | API | ✅ Yes | Apply for Elevated Access | Fully automated |
| **Facebook** | Playwright | ❌ No | Manual login once | Semi-automated |
| **Instagram** | Playwright | ❌ No | Manual login once | Semi-automated |
| LinkedIn | Playwright | ❌ No | Manual login once | Semi-automated |
| WhatsApp | Playwright | ❌ No | Manual login once | Semi-automated |

---

## Why This Hybrid Approach?

### Twitter API
- **Pros**: Fully automated, reliable, official support
- **Cons**: Requires API approval, rate limits
- **Best for**: High-volume posting, analytics, monitoring

### Playwright (Facebook/Instagram)
- **Pros**: No API approval needed, no API costs, works immediately
- **Cons**: Requires browser, session management, less reliable
- **Best for**: Personal accounts, occasional posting, avoiding API complexity

---

## Demo Mode

All platforms support **demo mode** for testing:

```bash
# Twitter demo mode (no API calls)
TWITTER_DEMO_MODE=true

# Facebook demo mode (no browser automation)
FACEBOOK_DEMO_MODE=true

# Instagram demo mode (no browser automation)
INSTAGRAM_DEMO_MODE=true
```

In demo mode:
- No real posts are made
- Actions are logged to console
- Useful for testing workflows
- No credentials needed

---

## Quick Start

### Option 1: Demo Mode (Test Everything)
```bash
# All platforms in demo mode by default
python main.py
```

### Option 2: Twitter Only (API)
```bash
# Configure Twitter API in .env
TWITTER_DEMO_MODE=false

# Other platforms stay in demo mode
FACEBOOK_DEMO_MODE=true
INSTAGRAM_DEMO_MODE=true
```

### Option 3: All Platforms (Hybrid)
```bash
# Configure Twitter API
TWITTER_DEMO_MODE=false

# First run: Log in to Facebook/Instagram manually
# Browser will open, log in, session saved
FACEBOOK_DEMO_MODE=false
INSTAGRAM_DEMO_MODE=false

# Future runs: Automatic using saved sessions
```

---

## Troubleshooting

### Twitter API Issues
- **401 Unauthorized**: Check API keys are correct
- **403 Forbidden**: Need Elevated Access
- **429 Rate Limit**: Wait and retry
- **Solution**: Verify credentials in Twitter Developer Portal

### Facebook/Instagram Playwright Issues
- **Session expired**: Delete `/sessions/facebook/` and log in again
- **Browser won't open**: Install Playwright: `playwright install chromium`
- **Login required**: Session expired, log in manually
- **Solution**: Run with `headless=False` to see what's happening

---

## Security Notes

### Twitter API
- Store keys in `.env` file
- Never commit `.env` to git
- Rotate keys monthly
- Use environment variables in production

### Playwright Sessions
- Sessions stored in `/sessions/` folder
- Contains authentication cookies
- Add `/sessions/` to `.gitignore`
- Delete sessions to force re-login

---

## Summary

**For Gold Tier, you only need:**

1. **Twitter API keys** (if using Twitter)
2. **Facebook/Instagram accounts** (for Playwright)
3. **Playwright installed**: `pip install playwright && playwright install chromium`

**No Facebook/Instagram API setup required!** 🎉

## Implementation Status

✅ **Twitter**: API-based implementation complete (tweepy)
✅ **Facebook**: Playwright-based implementation complete (no API keys)
✅ **Instagram**: Playwright-based implementation complete (no API keys)

All watchers and MCP servers now use the correct approach as specified.

---

*Last Updated: 2026-03-21*
