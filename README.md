# X Tweet Automation

Automated tweet posting from a queue on a scheduled basis using Android device automation.

## Quick Start

1. Setup:
```bash
cp .env_example .env
# Edit .env and add your device ID (from 'adb devices')
uv sync
```

2. Add tweets to queue:
```bash
uv run manage_tweets.py
```

3. Post manually:
```bash
uv run main.py
```

4. Setup cron for automatic posting:
```bash
# Edit lib/schedule_config.py to set posting times
# Add to crontab (runs every minute, posts only at scheduled times):
* * * * * cd /path/to/x-tweet-automation && uv run post_scheduler.py
```

## Usage

**Add/manage tweets:**
```bash
uv run manage_tweets.py
```

**Post next tweet manually:**
```bash
uv run main.py
```

**Scheduler (use with cron):**
```bash
uv run post_scheduler.py
```

## Project Structure

```
.
├── main.py              # Manual posting - posts next tweet
├── manage_tweets.py     # CLI to add/edit/delete tweets
├── post_scheduler.py    # Scheduler for automatic posting
├── lib/                 # Core modules
│   ├── device.py        # Android device connection
│   ├── x_automation.py  # X app automation
│   ├── tweet_db.py      # TinyDB database operations
│   └── schedule_config.py  # Posting schedule times
├── tweets.json          # Tweet queue database (auto-created)
└── .env                 # Device configuration
```

## Requirements

- Android device with USB debugging enabled
- X (Twitter) app installed
- Device connected via ADB
- Python 3.14+
