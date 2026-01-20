# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

X (Twitter) automation tool that posts tweets from a queue on a scheduled basis. Uses Android UI automation via uiautomator2 and ADB to interact with the X mobile app.

## Commands

```bash
# Install dependencies
uv sync

# Setup shell aliases (optional)
./setup_aliases.sh  # Shows aliases to add to ~/.zshrc

# With aliases (after adding to ~/.zshrc)
xt   # Manage tweets
xw   # Post next tweet

# Without aliases
uv run manage_tweets.py  # Manage tweets
uv run main.py           # Post next tweet
uv run post_scheduler.py # Scheduler for cron
```

## Configuration

**Environment** (`.env`):
- `DEVICE_ID`: ADB device identifier (get via `adb devices`)

**Posting schedule** (`lib/schedule_config.py`):
- Daily posting times in HH:MM format (24-hour)
- Default: 09:00, 14:00, 19:00

## Architecture

**Root scripts (user-facing):**
- `main.py` - Manually post next pending tweet from queue
- `manage_tweets.py` - CLI tool to add/edit/delete tweets
- `post_scheduler.py` - Scheduler for cron, posts at configured times

**Core modules (lib/):**
- `device.py` - Android device connection via ADB
- `x_automation.py` - X app automation (open app, compose, type, post)
- `tweet_db.py` - TinyDB operations for tweet queue
- `schedule_config.py` - Posting schedule configuration

## Tweet Queue System

**Database:** TinyDB (NoSQL JSON) in `tweets.json`

**Tweet structure:**
- text: Tweet content (max 280 chars)
- status: pending/posted
- posted_at: Timestamp when posted
- created_at: When added to queue

**Workflow:**
1. Add tweets via `manage_tweets.py`
2. Run `main.py` manually OR setup cron with `post_scheduler.py`
3. Scheduler checks if current time matches posting schedule
4. If match, posts next pending tweet
5. Tweet marked as posted with timestamp

**Character limit:** 280 chars validated on add/edit

## X Automation Flow

1. Stop all apps on device
2. Open X app (click app icon)
3. Open composer (double-click compose button)
4. Click text area at (180, 500)
5. Type tweet using fastinput_ime
6. Click post button at (928, 192)
7. Wait 15 seconds for posting to complete

## Scheduler Setup (macOS)

Uses launchd instead of cron:

```bash
# Setup (one-time)
./setup_scheduler.sh

# Manage
launchctl list | grep xtweet              # Check status
launchctl unload ~/Library/LaunchAgents/com.xtweet.scheduler.plist  # Stop
launchctl load ~/Library/LaunchAgents/com.xtweet.scheduler.plist    # Start
tail -f logs/scheduler.log                # View logs
```

Configuration file: `com.xtweet.scheduler.plist`
- Runs every 60 seconds
- Posts only at times defined in `lib/schedule_config.py`
- Logs to `logs/scheduler.log` and `logs/scheduler_error.log`

## Database

TinyDB stores tweets in `tweets.json` (excluded from git). View/edit with any JSON viewer or use the CLI tool.

Tweet structure:
```json
{
  "text": "Tweet content with #hashtags included in text",
  "status": "pending",
  "posted_at": null,
  "created_at": "2026-01-19T12:00:00"
}
```
