# X Tweet Automation

![Python](https://img.shields.io/badge/python-3.14+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Platform](https://img.shields.io/badge/platform-Android-brightgreen.svg)
![Status](https://img.shields.io/badge/status-active-success.svg)

> Automated tweet posting from a queue on a scheduled basis using Android device automation via ADB.

## Features

- **Queue-based posting** - Add multiple tweets, post them automatically
- **Flexible scheduling** - Configure daily posting times
- **Manual control** - Post tweets manually or via cron scheduler
- **Character validation** - Automatic 280-character limit checking
- **Hashtag support** - Auto-formatted hashtags
- **Simple CLI** - Easy-to-use command-line interface
- **NoSQL database** - TinyDB for lightweight tweet storage

## Prerequisites

- Python 3.14 or higher
- Android device with USB debugging enabled
- X (Twitter) app installed on device
- ADB connection (USB or wireless)
- Device ID from `adb devices` command

## Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd x-tweet-automation
   ```

2. **Install dependencies**
   ```bash
   uv sync
   ```

3. **Configure environment**
   ```bash
   cp .env_example .env
   # Edit .env and add your device ID
   ```

4. **Get your device ID**
   ```bash
   adb devices
   # Copy the device ID and paste it in .env
   ```

## Quick Start

### 1. Add Tweets to Queue

```bash
uv run manage_tweets.py
```

Follow the interactive prompts to add tweets with hashtags.

### 2. Post Manually

Post the next tweet in queue:

```bash
uv run main.py
```

### 3. Schedule Automatic Posting

Edit posting times in `lib/schedule_config.py`:

```python
POSTING_SCHEDULE = [
    "09:00",
    "14:00",
    "19:00"
]
```

Add to crontab:

```bash
crontab -e
# Add this line:
* * * * * cd /path/to/x-tweet-automation && uv run post_scheduler.py
```

The scheduler runs every minute but only posts at configured times.

## Usage

### Managing Tweets

```bash
uv run manage_tweets.py
```

**Options:**
1. Add tweet to queue
2. List all tweets
3. List pending queue
4. Edit tweet
5. Delete tweet
6. Show posting schedule
7. Exit

### Manual Posting

```bash
uv run main.py
```

Posts the next pending tweet from the queue immediately.

### Scheduler

```bash
uv run post_scheduler.py
```

Checks current time against schedule and posts if there's a match.

## Project Structure

```
.
├── main.py                  # Manual posting script
├── manage_tweets.py         # Tweet management CLI
├── post_scheduler.py        # Automated scheduler
├── lib/                     # Core library
│   ├── device.py           # ADB device connection
│   ├── x_automation.py     # X app automation
│   ├── tweet_db.py         # Database operations
│   └── schedule_config.py  # Posting schedule
├── tweets.json             # Tweet queue (auto-created)
├── .env                    # Device configuration
└── README.md              # This file
```

## Configuration

### Environment Variables (`.env`)

```env
DEVICE_ID=your_device_id_here
```

### Posting Schedule (`lib/schedule_config.py`)

```python
POSTING_SCHEDULE = ["09:00", "14:00", "19:00"]
```

Times are in 24-hour format (HH:MM).

## How It Works

1. **Queue System** - Tweets are stored in a queue with status tracking
2. **Scheduling** - Define specific times for automatic posting
3. **Automation** - Uses uiautomator2 to interact with X app via ADB
4. **Posting Flow**:
   - Connect to Android device
   - Stop all apps
   - Open X app
   - Open tweet composer
   - Type tweet text with hashtags
   - Click post button
   - Wait for posting to complete
   - Mark tweet as posted

## Examples

### Adding a Tweet

```
Tweet text: Standing with the people of Iran
Hashtags (comma-separated, no #): FreeIran,Iran2026
```

Result: `Standing with the people of Iran #FreeIran #Iran2026`

### Viewing Queue

```
=== Tweets (pending) (2) ===

ID: 1 | Status: pending | 42/280 chars
   Standing with the people of Iran #FreeIran

ID: 2 | Status: pending | 55/280 chars
   The resilience of the Iranian people is inspiring #Iran
```

## Troubleshooting

**Device not connecting?**
- Check USB debugging is enabled
- Verify device is authorized: `adb devices`
- Try reconnecting the device

**Tweet not posting?**
- Ensure X app is installed
- Check device coordinates match your screen
- Verify tweet length is under 280 characters

**Scheduler not posting?**
- Check current time matches schedule
- Verify cron job is running: `crontab -l`
- Check logs if redirected

## License

MIT License - feel free to use and modify.

## Contributing

Contributions are welcome! Feel free to submit issues or pull requests.

---

**Built with** Python • uiautomator2 • TinyDB • ADB
