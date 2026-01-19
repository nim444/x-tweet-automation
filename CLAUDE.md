# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

X (Twitter) automation tool that posts tweets from a queue on a scheduled basis. Uses Android UI automation via uiautomator2 and ADB to interact with the X mobile app.

## Commands

```bash
# Install dependencies
uv sync

# Manage tweet queue (add, edit, delete tweets)
uv run manage_tweets.py

# Post next pending tweet manually
uv run main.py

# Run scheduler (for cron) - posts at scheduled times
uv run post_scheduler.py
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
- text: Tweet content
- hashtags: Comma-separated (auto-formatted with #)
- status: pending/posted
- posted_at: Timestamp when posted
- created_at: When added to queue

**Workflow:**
1. Add tweets via `manage_tweets.py`
2. Run `main.py` manually OR setup cron with `post_scheduler.py`
3. Scheduler checks if current time matches posting schedule
4. If match, posts next pending tweet
5. Tweet marked as posted with timestamp

**Character limit:** 280 chars (text + hashtags validated)

## X Automation Flow

1. Stop all apps on device
2. Open X app (click app icon)
3. Open composer (double-click compose button)
4. Click text area at (180, 500)
5. Type tweet using fastinput_ime
6. Click post button at (928, 192)
7. Wait 15 seconds for posting to complete

## Cron Setup

```bash
# Run every minute, posts only at scheduled times
* * * * * cd /path/to/project && uv run post_scheduler.py >> logs/scheduler.log 2>&1
```

## Database Viewing

View `tweets.json` with any JSON viewer or use `manage_tweets.py` CLI.
