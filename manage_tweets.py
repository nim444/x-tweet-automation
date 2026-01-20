"""CLI tool to manage tweets."""
from lib.tweet_db import TweetDB
from lib.schedule_config import POSTING_SCHEDULE


def add_tweet(db: TweetDB):
    """Add a new tweet to queue."""
    print("\n=== Add Tweet to Queue ===")
    text = input("Tweet text: ").strip()

    try:
        tweet_id = db.add_tweet(text)
        tweet = db.get_tweet(tweet_id)
        full_text = db.get_full_text(tweet)
        print(f"\nAdded to queue - ID: {tweet_id}")
        print(f"Preview: {full_text}")
        print(f"Length: {len(full_text)}/280")
    except ValueError as e:
        print(f"\nError: {e}")


def list_tweets(db: TweetDB, filter_status=None):
    """List all tweets."""
    tweets = db.get_all_tweets(status=filter_status)

    if not tweets:
        print("\nNo tweets found")
        return

    status_filter = f" ({filter_status})" if filter_status else ""
    print(f"\n=== Tweets{status_filter} ({len(tweets)}) ===\n")

    for tweet in tweets:
        full_text = db.get_full_text(tweet)
        print(f"ID: {tweet.doc_id} | Status: {tweet['status']} | {len(full_text)}/280 chars")
        print(f"   {full_text}")
        print()


def edit_tweet(db: TweetDB):
    """Edit an existing tweet."""
    tweet_id = input("\nEnter tweet ID: ").strip()
    if not tweet_id.isdigit():
        print("Invalid ID")
        return

    tweet_id = int(tweet_id)
    tweet = db.get_tweet(tweet_id)

    if not tweet:
        print(f"Tweet {tweet_id} not found")
        return

    print(f"\nCurrent: {db.get_full_text(tweet)}")

    text = input("\nNew text: ").strip()

    if not text:
        print("No changes made")
        return

    try:
        db.update_tweet(tweet_id, text)
        updated = db.get_tweet(tweet_id)
        full_text = db.get_full_text(updated)
        print(f"\nUpdated ({len(full_text)}/280)")
        print(f"Preview: {full_text}")
    except ValueError as e:
        print(f"\nError: {e}")


def delete_tweet(db: TweetDB):
    """Delete a tweet."""
    tweet_id = input("\nEnter tweet ID: ").strip()
    if not tweet_id.isdigit():
        print("Invalid ID")
        return

    tweet_id = int(tweet_id)
    tweet = db.get_tweet(tweet_id)

    if not tweet:
        print(f"Tweet {tweet_id} not found")
        return

    print(f"\nDelete: {db.get_full_text(tweet)}")
    confirm = input("Type 'yes' to confirm: ").strip().lower()

    if confirm == 'yes':
        db.delete_tweet(tweet_id)
        print("Deleted")
    else:
        print("Cancelled")


def show_schedule():
    """Show posting schedule."""
    print("\n=== Posting Schedule ===")
    print("Daily posting times:")
    for time in POSTING_SCHEDULE:
        print(f"  - {time}")
    print("\nEdit schedule_config.py to change times")


def main():
    """Main CLI menu."""
    db = TweetDB()

    try:
        while True:
            print("\n" + "="*40)
            print("Tweet Manager")
            print("="*40)
            print("1. Add tweet to queue")
            print("2. List all tweets")
            print("3. List pending queue")
            print("4. Edit tweet")
            print("5. Delete tweet")
            print("6. Show posting schedule")
            print("7. Exit")

            choice = input("\nChoice: ").strip()

            if choice == '1':
                add_tweet(db)
            elif choice == '2':
                list_tweets(db)
            elif choice == '3':
                list_tweets(db, 'pending')
            elif choice == '4':
                edit_tweet(db)
            elif choice == '5':
                delete_tweet(db)
            elif choice == '6':
                show_schedule()
            elif choice == '7':
                break
            else:
                print("Invalid option")
    finally:
        db.close()


if __name__ == "__main__":
    main()
