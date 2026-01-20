"""Tweet database using TinyDB."""

from tinydb import TinyDB, Query
from datetime import datetime
from typing import List, Optional


class TweetDB:
    """Manages tweets in TinyDB (NoSQL JSON database)."""

    def __init__(self, db_file: str = "tweets.json"):
        self.db = TinyDB(db_file, indent=2)
        self.tweets = self.db.table("tweets")

    def validate_length(self, text: str) -> tuple[bool, int]:
        """
        Validate tweet length (≤ 280 chars).
        Returns: (is_valid, total_length)
        """
        length = len(text)
        return length <= 280, length

    def add_tweet(self, text: str) -> int:
        """Add a new tweet to queue. Returns tweet ID."""
        is_valid, length = self.validate_length(text)

        if not is_valid:
            raise ValueError(f"Tweet too long ({length}/280 characters)")

        tweet_id = self.tweets.insert(
            {
                "text": text,
                "status": "pending",
                "posted_at": None,
                "created_at": datetime.now().isoformat(),
            }
        )

        return tweet_id

    def get_all_tweets(self, status: Optional[str] = None) -> List[dict]:
        """Get all tweets, optionally filtered by status."""
        if status:
            Tweet = Query()
            return self.tweets.search(Tweet.status == status)
        return self.tweets.all()

    def get_tweet(self, tweet_id: int) -> Optional[dict]:
        """Get a specific tweet by ID."""
        return self.tweets.get(doc_id=tweet_id)

    def update_tweet(self, tweet_id: int, text: str) -> bool:
        """Update a tweet's text."""
        tweet = self.get_tweet(tweet_id)
        if not tweet:
            return False

        # Validate
        is_valid, length = self.validate_length(text)
        if not is_valid:
            raise ValueError(f"Tweet too long ({length}/280 characters)")

        self.tweets.update({"text": text}, doc_ids=[tweet_id])
        return True

    def delete_tweet(self, tweet_id: int) -> bool:
        """Delete a tweet."""
        return bool(self.tweets.remove(doc_ids=[tweet_id]))

    def mark_as_posted(self, tweet_id: int) -> bool:
        """Mark a tweet as posted."""
        self.tweets.update(
            {"status": "posted", "posted_at": datetime.now().isoformat()},
            doc_ids=[tweet_id],
        )
        return True

    def get_next_pending(self) -> Optional[dict]:
        """Get the next pending tweet to post."""
        Tweet = Query()
        pending = self.tweets.search(Tweet.status == "pending")
        return pending[0] if pending else None

    def get_full_text(self, tweet: dict) -> str:
        """Get full text for a tweet."""
        return tweet["text"]

    def close(self):
        """Close database connection."""
        self.db.close()
