"""Main entry point for X tweet automation - posts next pending tweet."""

import os
from dotenv import load_dotenv
from time import sleep

from lib.device import Device
from lib.x_automation import XAutomation
from lib.tweet_db import TweetDB


def main():
    # Load environment variables
    load_dotenv()
    device_id = os.getenv("DEVICE_ID", "")

    if not device_id:
        print("Error: DEVICE_ID not set in .env file")
        return

    # Get next pending tweet from queue
    db = TweetDB()
    tweet = db.get_next_pending()

    if not tweet:
        print("No pending tweets in queue")
        db.close()
        return

    tweet_text = db.get_full_text(tweet)
    print(f"Posting tweet ID {tweet.doc_id}")
    print(f"Text: {tweet_text}")
    print(f"Length: {len(tweet_text)}/280")

    # Connect to device
    device = Device(device_id)
    if not device.connect():
        db.close()
        return

    # Stop all apps
    device.stop_all_apps()

    # Start X automation
    x_auto = XAutomation(device.device)

    # Open X app and composer
    success = False
    if x_auto.open_x_app():
        if x_auto.open_composer():
            if x_auto.write_and_post_tweet(tweet_text):
                success = True

    # Mark as posted if successful
    if success:
        db.mark_as_posted(tweet.doc_id)
        print(f"Tweet {tweet.doc_id} posted successfully")
    else:
        print("Failed to post tweet")

    # Wait for tweet to fully post
    print("Waiting for tweet to finish posting...")
    sleep(15)

    db.close()
    print("Automation completed")


if __name__ == "__main__":
    main()
