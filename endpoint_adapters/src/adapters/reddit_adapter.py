"""Reddit Adapter."""

import logging
from os import getenv

from praw.reddit import Reddit
from praw.models import SubredditMessage
from prawcore.exceptions import ResponseException

from adapters.base_adapter import AbstractAdapter


MAX_SUBREDDITS = 10
MAX_POSTS = 100

# TODO: Build a proper query.
SEARCH_QUERY = "movie"


class RedditAdapter(AbstractAdapter):
    """Adapter for Reddit."""

    _list_of_titles: list[str]

    def __init__(self, publish: callable):
        super().__init__(publish)
        self.reddit = self.__build_reddit_instance()
        logging.info("Initialized Reddit instance.")
        self.relevant_subreddits = self.__fetch_relevant_subreddits()
        logging.info('Found %s relevant subreddits: [%s]',
                     len(self.relevant_subreddits), ", ".join(self.relevant_subreddits))

    def __build_reddit_instance(self) -> Reddit:
        """Factory method for reddit instance."""
        return Reddit(
            client_id=getenv("REDDIT_CLIENT_ID"),
            client_secret=getenv("REDDIT_CLIENT_SECRET"),
            user_agent=getenv("REDDIT_USER_AGENT"))

    def __fetch_relevant_subreddits(self) -> list:
        """Fetch relevant subreddits."""
        return [subreddit.display_name for subreddit in
                self.reddit.subreddits.search(SEARCH_QUERY,
                                              limit=MAX_SUBREDDITS)
                if subreddit.subreddit_type == "public"]

    def set_list_of_titles(self, list_of_titles: list[str]):
        """Setter for list of titles."""
        self._list_of_titles = list_of_titles

    def fetch(self):
        for title in self._list_of_titles:
            logging.info('Searching for \"%s\" in subreddits.', title)
            try:
                posts = self.__find_posts(title)
            except ResponseException as exception:
                logging.error(
                    'Error while searching for \"%s\" in subreddits: %s.',
                    title, exception.response)
                continue
            logging.info('Found %s posts for \"%s\" in subreddits.',
                         len(posts), title)
            self.__publish_posts(posts)

    def __find_posts(self, title: str) -> list[str]:
        subreddits = "+".join(self.relevant_subreddits)
        results = self.reddit.subreddit(subreddits).search(
            query=title, sort="relevance", limit=MAX_POSTS)
        # TODO: if we want to track more details, we should add that here.
        # TODO: if we want to track comments as well, we should add that here.
        results = [submission.selftext.strip() for submission in results]
        posts = [submission for submission in results if submission != ""]
        return posts

    def __publish_posts(self, posts: list[SubredditMessage]):
        """Publishes the reviews to the message queue."""
        logging.info('Publishing %s posts to message queue.', len(posts))
        for post in posts:
            # TODO: add logic for e.g. weighting reviews here.
            self.publish(post)
