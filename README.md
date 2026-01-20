# X Tweet Automation

![Python](https://img.shields.io/badge/python-3.14+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Platform](https://img.shields.io/badge/platform-Android-brightgreen.svg)
![Status](https://img.shields.io/badge/status-active-success.svg)


![x-tweet](tx.gif)


> Automated tweet posting from a queue on a scheduled basis using Android device automation via ADB.

## Features

- **Queue-based posting** - Add multiple tweets, post them automatically
- **Flexible scheduling** - Configure daily posting times
- **Manual control** - Post tweets manually or via scheduler
- **Character validation** - Automatic 280-character limit checking
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

### 1. Setup Shell Aliases (Optional but Recommended)

Run the setup script:

```bash
./setup_aliases.sh
```

Copy the output and add to your `~/.zshrc`, then reload:

```bash
source ~/.zshrc
```

Now you can use:
```bash
xt   # Manage tweets (add, edit, delete)
xw   # Post next tweet manually
```

### 2. Add Tweets to Queue

```bash
xt
# OR without alias:
uv run manage_tweets.py
```

Enter your tweet text (max 280 characters).

### 3. Post Manually

Post the next tweet in queue:

```bash
xw
# OR without alias:
uv run main.py
```

### 4. Schedule Automatic Posting (macOS)

Edit posting times in `lib/schedule_config.py`:

```python
POSTING_SCHEDULE = [
    "09:00",
    "14:00",
    "19:00"
]
```

Setup the scheduler using launchd (macOS native):

```bash
./setup_scheduler.sh
```

This will:
- Install the scheduler to run every 60 seconds
- Only post tweets at configured times
- Start automatically on login
- Log to `logs/scheduler.log`

**Manage the scheduler:**
```bash
# Check if running
launchctl list | grep xtweet

# View logs
tail -f logs/scheduler.log

# Stop scheduler
launchctl unload ~/Library/LaunchAgents/com.xtweet.scheduler.plist

# Start scheduler
launchctl load ~/Library/LaunchAgents/com.xtweet.scheduler.plist
```

## Usage

### Managing Tweets

```bash
xt
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
xw
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
├── main.py                      # Manual posting script
├── manage_tweets.py             # Tweet management CLI
├── post_scheduler.py            # Automated scheduler
├── setup_aliases.sh             # Shell alias setup
├── setup_scheduler.sh           # macOS scheduler setup
├── com.xtweet.scheduler.plist   # launchd configuration
├── lib/                         # Core library
│   ├── device.py               # ADB device connection
│   ├── x_automation.py         # X app automation
│   ├── tweet_db.py             # Database operations
│   └── schedule_config.py      # Posting schedule
├── tweets.json                 # Tweet queue (auto-created)
├── logs/                       # Scheduler logs (auto-created)
├── .env                        # Device configuration
└── README.md                   # This file
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

Times in 24-hour format (HH:MM). The scheduler runs every 60 seconds but only posts at these times.

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
Tweet text: Standing with the people of Iran #FreeIran
```

Result: Tweet added to queue with 42/280 characters

### Viewing Queue

```
=== Tweets (pending) (2) ===

ID: 1 | Status: pending | 42/280 chars
   Standing with the people of Iran #FreeIran

ID: 2 | Status: pending | 66/280 chars
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
