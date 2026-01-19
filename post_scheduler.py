"""Scheduler to post tweets at configured times."""
import os
from datetime import datetime
from dotenv import load_dotenv

from tweet_db import TweetDB
from device import Device
from x_automation import XAutomation
from schedule_config import POSTING_SCHEDULE


def should_post_now() -> bool:
    """Check if current time matches any posting schedule."""
    now = datetime.now()
    current_time = now.strftime("%H:%M")
    return current_time in POSTING_SCHEDULE


def post_tweet(device, tweet_text: str) -> bool:
    """Post a tweet using X automation."""
    try:
        x_auto = XAutomation(device)

        if not x_auto.open_x_app():
            return False

        if not x_auto.open_composer():
            return False

        # TODO: Type the tweet text and post
        # This needs to be implemented in x_automation.py
        print(f"Would post: {tweet_text}")

        return True
    except Exception as e:
        print(f"Failed to post: {e}")
        return False


def main():
    """Main scheduler entry point."""
    load_dotenv()
    device_id = os.getenv('DEVICE_ID', '')

    if not device_id:
        print("Error: DEVICE_ID not set")
        return

    # Check if it's time to post
    if not should_post_now():
        print(f"Not a scheduled time. Next posts at: {', '.join(POSTING_SCHEDULE)}")
        return

    # Get next pending tweet
    db = TweetDB()
    tweet = db.get_next_pending()

    if not tweet:
        print("No pending tweets in queue")
        db.close()
        return

    tweet_text = db.get_full_text(tweet)
    print(f"Posting tweet ID {tweet.doc_id}: {tweet_text}")

    # Connect to device
    device = Device(device_id)
    if not device.connect():
        db.close()
        return

    device.stop_all_apps()

    # Post the tweet
    if post_tweet(device.device, tweet_text):
        db.mark_as_posted(tweet.doc_id)
        print("Tweet posted successfully")
    else:
        print("Failed to post tweet")

    db.close()


if __name__ == "__main__":
    main()
