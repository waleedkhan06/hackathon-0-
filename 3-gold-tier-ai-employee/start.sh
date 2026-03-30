#!/bin/bash
# AI Employee - Production Startup Script
# Starts all watchers and monitors system health

cd /mnt/e/hackathon-0-ai-employee/silver-tier-ai-employee
source venv/bin/activate

echo ""
echo "============================================================"
echo "🤖 AI EMPLOYEE SILVER TIER - STARTING UP"
echo "============================================================"
echo ""

# Check if already running
if pgrep -f "gmail_watcher.py" > /dev/null; then
    echo "⚠️  Gmail watcher already running"
else
    echo "📧 Starting Gmail Watcher..."
    python watchers/gmail_watcher.py &
    sleep 2
    echo "    ✓ Gmail watcher started"
fi

if pgrep -f "whatsapp_watcher.py" > /dev/null; then
    echo "⚠️  WhatsApp watcher already running"
else
    echo "💬 Starting WhatsApp Watcher..."
    python watchers/whatsapp_watcher.py &
    sleep 2
    echo "    ✓ WhatsApp watcher started"
fi

if pgrep -f "linkedin_watcher.py" > /dev/null; then
    echo "⚠️  LinkedIn watcher already running"
else
    echo "📱 Starting LinkedIn Watcher..."
    python watchers/linkedin_watcher.py &
    sleep 2
    echo "    ✓ LinkedIn watcher started"
fi

echo ""
echo "============================================================"
echo "✅ ALL WATCHERS RUNNING!"
echo "============================================================"
echo ""
echo "📋 Quick Commands:"
echo "  Check pending:  ls pending_approval/"
echo "  Approve all:    mv pending_approval/*.md approved/"
echo "  Stop all:       pkill -f watcher"
echo "  View logs:      tail -f logs/*_watcher_*.log"
echo ""
echo "📁 Working Folders:"
echo "  needs_action/      - Auto-processed items"
echo "  pending_approval/  - Needs your approval"
echo "  approved/          - Ready to execute"
echo "  done/              - Completed items"
echo ""
echo "============================================================"
echo ""
