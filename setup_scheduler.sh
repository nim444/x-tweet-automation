#!/bin/bash
# Setup launchd scheduler for macOS

PROJECT_DIR="/Users/nk/Projects/26/x-tweet-automation"
PLIST_FILE="com.xtweet.scheduler.plist"
LAUNCH_AGENTS_DIR="$HOME/Library/LaunchAgents"

echo "=== X Tweet Automation - macOS Scheduler Setup ==="
echo ""

# Create LaunchAgents directory if it doesn't exist
mkdir -p "$LAUNCH_AGENTS_DIR"

# Copy plist file
echo "1. Copying scheduler configuration..."
cp "$PROJECT_DIR/$PLIST_FILE" "$LAUNCH_AGENTS_DIR/$PLIST_FILE"
echo "   ✓ Copied to $LAUNCH_AGENTS_DIR"

# Load the job
echo ""
echo "2. Loading scheduler..."
launchctl unload "$LAUNCH_AGENTS_DIR/$PLIST_FILE" 2>/dev/null
launchctl load "$LAUNCH_AGENTS_DIR/$PLIST_FILE"
echo "   ✓ Scheduler loaded"

echo ""
echo "3. Scheduler is now active!"
echo "   - Runs every 60 seconds"
echo "   - Posts only at times configured in lib/schedule_config.py"
echo "   - Logs: $PROJECT_DIR/logs/"
echo ""
echo "Commands:"
echo "  launchctl list | grep xtweet        # Check if running"
echo "  tail -f logs/scheduler.log          # View logs"
echo "  launchctl unload ~/Library/LaunchAgents/$PLIST_FILE  # Stop scheduler"
echo "  launchctl load ~/Library/LaunchAgents/$PLIST_FILE    # Start scheduler"
echo ""
