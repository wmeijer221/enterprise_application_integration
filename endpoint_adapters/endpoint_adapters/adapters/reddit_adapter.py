"""Reddit Adapter."""

import logging
from os import getenv
import datetime
from uuid import NAMESPACE_OID, uuid3, uuid4

from praw.reddit import Reddit
from praw.models import SubredditMessage
from prawcore.exceptions import ResponseException

from base.canonical_model import Review, Title
from endpoint_adapters.adapters import APIAdapter

MAX_SUBREDDITS = 10
MAX_POSTS = 100

# TODO: Build a proper query.
SEARCH_QUERY = "movie"


class RedditAdapter(APIAdapter):
    """Adapter for Reddit."""

    def __init__(self, publish: callable):
        super().__init__(publish)
        self.reddit = self.__build_reddit_instance()
        logging.debug("Initialized Reddit instance.")
        self.relevant_subreddits = self.__fetch_relevant_subreddits()
        logging.debug(
            "Found %s relevant subreddits: [%s]",
            len(self.relevant_subreddits),
            ", ".join(self.relevant_subreddits),
        )

    def __build_reddit_instance(self) -> Reddit:
        """Factory method for reddit instance."""
        # Get your client ID / Secret here: https://ssl.reddit.com/prefs/apps/
        return Reddit(
            client_id=getenv("REDDIT_CLIENT_ID"),
            client_secret=getenv("REDDIT_CLIENT_SECRET"),
            user_agent=getenv("REDDIT_USER_AGENT"),
        )

    def __fetch_relevant_subreddits(self) -> list:
        """Fetch relevant subreddits."""
        return [
            subreddit.display_name
            for subreddit in self.reddit.subreddits.search(
                SEARCH_QUERY, limit=MAX_SUBREDDITS
            )
            if subreddit.subreddit_type == "public"
        ]


    def fetch_title(self, title: Title):
        logging.debug('Searching for "%s" in subreddits.', title)
        try:
            posts = self.__find_posts(title.name)
        except ResponseException as exception:
            logging.error(
                'Error while searching for "%s" in subreddits: %s.',
                title,
                exception.response,
            )
            return
        logging.debug('Found %s posts for "%s" in subreddits.', len(posts), title)
        self.__publish_posts(title, posts)


    def __find_posts(self, title: str) -> "list[SubredditMessage]":
        subreddits = "+".join(self.relevant_subreddits)
        results = self.reddit.subreddit(subreddits).search(
            query=title, sort="relevance", limit=MAX_POSTS
        )
        # TODO: if we want to track more details, we should add that here.
        # TODO: if we want to track comments as well, we should add that here.
        posts = [
            submission for submission in results if submission.selftext.strip() != ""
        ]
        return posts

    def __publish_posts(self, title: Title, posts: "list[SubredditMessage]"):
        """Publishes the reviews to the message queue."""
        logging.debug("Publishing %s posts to message queue.", len(posts))
        for post in posts:
            timestamp = datetime.datetime.fromtimestamp(post.created_utc)
            review = Review(
                str(uuid3(NAMESPACE_OID, post.selftext + str(post.author))),
                title_id=title.uuid,
                text=post.selftext,
                source_name="reddit",
                source_id=f'{str(post.subreddit)}/{str(post.id)}',
                timestamp=str(timestamp),
                reviewer=str(post.author),
            )
            self.publish(review)
