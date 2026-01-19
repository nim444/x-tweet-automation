"""Tweet database using TinyDB."""
from tinydb import TinyDB, Query
from datetime import datetime
from typing import List, Optional


class TweetDB:
    """Manages tweets in TinyDB (NoSQL JSON database)."""

    def __init__(self, db_file: str = "tweets.json"):
        self.db = TinyDB(db_file, indent=2)
        self.tweets = self.db.table('tweets')

    def validate_length(self, text: str, hashtags: str) -> tuple[bool, int]:
        """
        Validate tweet length (text + hashtags ≤ 280 chars).
        Returns: (is_valid, total_length)
        """
        full_text = self._format_full_text(text, hashtags)
        length = len(full_text)
        return length <= 280, length

    def _format_full_text(self, text: str, hashtags: str) -> str:
        """Format full tweet text with hashtags."""
        if hashtags:
            tags = ' '.join(f'#{tag.strip()}' for tag in hashtags.split(',') if tag.strip())
            return f"{text} {tags}".strip()
        return text

    def add_tweet(self, text: str, hashtags: str = "") -> int:
        """Add a new tweet to queue. Returns tweet ID."""
        is_valid, length = self.validate_length(text, hashtags)

        if not is_valid:
            raise ValueError(f"Tweet too long ({length}/280 characters)")

        tweet_id = self.tweets.insert({
            'text': text,
            'hashtags': hashtags,
            'status': 'pending',
            'posted_at': None,
            'created_at': datetime.now().isoformat()
        })

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

    def update_tweet(self, tweet_id: int, text: Optional[str] = None,
                     hashtags: Optional[str] = None) -> bool:
        """Update a tweet's text or hashtags."""
        tweet = self.get_tweet(tweet_id)
        if not tweet:
            return False

        # Prepare updates
        updates = {}
        new_text = text if text is not None else tweet['text']
        new_hashtags = hashtags if hashtags is not None else tweet['hashtags']

        # Validate
        is_valid, length = self.validate_length(new_text, new_hashtags)
        if not is_valid:
            raise ValueError(f"Tweet too long ({length}/280 characters)")

        if text is not None:
            updates['text'] = text
        if hashtags is not None:
            updates['hashtags'] = hashtags

        self.tweets.update(updates, doc_ids=[tweet_id])
        return True

    def delete_tweet(self, tweet_id: int) -> bool:
        """Delete a tweet."""
        return bool(self.tweets.remove(doc_ids=[tweet_id]))

    def mark_as_posted(self, tweet_id: int) -> bool:
        """Mark a tweet as posted."""
        self.tweets.update({
            'status': 'posted',
            'posted_at': datetime.now().isoformat()
        }, doc_ids=[tweet_id])
        return True

    def get_next_pending(self) -> Optional[dict]:
        """Get the next pending tweet to post."""
        Tweet = Query()
        pending = self.tweets.search(Tweet.status == 'pending')
        return pending[0] if pending else None

    def get_full_text(self, tweet: dict) -> str:
        """Get formatted full text for a tweet."""
        return self._format_full_text(tweet['text'], tweet['hashtags'])

    def close(self):
        """Close database connection."""
        self.db.close()
