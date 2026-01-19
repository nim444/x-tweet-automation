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

# Run scheduler to post next tweet (if current time matches schedule)
uv run post_scheduler.py

# Test device connection and X app opening
uv run main.py
```

## Configuration

**Environment variables** (`.env` file):
- `DEVICE_ID`: ADB device identifier (get via `adb devices`)

**Posting schedule** (`schedule_config.py`):
- Define daily posting times in HH:MM format (24-hour)
- Default: 09:00, 14:00, 19:00

## Architecture

**Core modules:**
- `device.py` - Android device connection and management via ADB
- `x_automation.py` - X app interaction logic (open app, open composer)
- `tweet_db.py` - Tweet queue database using TinyDB (NoSQL JSON)
- `manage_tweets.py` - CLI tool to manage tweet queue
- `post_scheduler.py` - Scheduler script that posts next pending tweet
- `schedule_config.py` - Posting schedule configuration
- `main.py` - Simple test script for device connection

**Tweet queue system:**
- Tweets stored in `tweets.json` (TinyDB)
- Each tweet has: text, hashtags, status (pending/posted), timestamps
- No individual scheduling - tweets posted from queue at configured times
- Hashtags are comma-separated, auto-formatted with # prefix
- 280 character limit validation (text + hashtags)

**Posting workflow:**
1. Add tweets to queue via `manage_tweets.py`
2. Run `post_scheduler.py` (via cron every minute)
3. Scheduler checks if current time matches posting schedule
4. If match, posts next pending tweet from queue
5. Tweet marked as 'posted' with timestamp

## Cron Setup

Run scheduler every minute:
```
* * * * * cd /path/to/project && /path/to/uv run post_scheduler.py >> /path/to/logs/scheduler.log 2>&1
```

## Database

TinyDB stores tweets in `tweets.json` (excluded from git). View/edit with any JSON viewer or use the CLI tool.

Tweet structure:
```json
{
  "text": "Tweet content",
  "hashtags": "tag1,tag2",
  "status": "pending",
  "posted_at": null,
  "created_at": "2026-01-19T12:00:00"
}
```
