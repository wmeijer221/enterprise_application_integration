import datetime
import logging
from os import getenv
import time
import requests
from uuid import NAMESPACE_OID, uuid3, uuid4

from base.canonical_model import Review, Title

from endpoint_adapters.adapters import APIAdapter

bearer_token = getenv("TWITTER_BEARER_TOKEN")


def bearer_oauth(r):
    """
    Method required by bearer token authentication.
    """

    r.headers["Authorization"] = f"Bearer {bearer_token}"
    r.headers["User-Agent"] = "MySentimentAnalysisTool"
    return r


class TestAdapter(APIAdapter):
    """Adapter for Twitter."""

    def fetch_title(self, title: Title):
        try:
            # Fetch tweets for title.
            posts = self.__find_posts(title.name)
        except Exception as exception:
            logging.error(
                'Error while searching for "%s" in tweets: %s.',
                title.name,
                exception,
            )
            return

        logging.debug('Found %s tweets for "%s".', len(posts), title)

        self.__publish_posts(title, posts)

    def __find_posts(self, title: str) -> "list[TwitterMessage]":
        # Wait 5 seconds to avoid rate limit.
        time.sleep(5)

        # Escape special url characters.
        title = title.replace(":", "")

        logging.info("Searching for %s in tweets.", title)
        response = requests.get(
            "https://api.twitter.com/2/tweets/search/recent",
            auth=bearer_oauth,
            # All fields can be found here: https://developer.twitter.com/en/docs/twitter-api/fields
            params={
                "query": title,
                "max_results": 10,
                "tweet.fields": "id,text,author_id,created_at",
                "user.fields": "id,name,username",
                "expansions": "author_id",
            },
        )

        if response.status_code != 200:
            raise Exception(response.status_code, response.text)

        response_json = response.json()

        tweets = response_json["data"]
        users = response_json["includes"]["users"]

        # Add user and place information to tweets.
        for tweet in tweets:
            user_id = tweet["author_id"]

            user = next(user for user in users if user["id"] == user_id)
            tweet["user"] = user

        return response_json["data"]

    def __publish_posts(self, title: Title, posts: "list[TwitterMessage]"):
        """Publishes the reviews to the message queue."""
        logging.debug("Publishing %s posts to message queue.", len(posts))
        for post in posts:
            timestamp = datetime.datetime.fromisoformat(post["created_at"][0:19])

            author = str(post["user"]["name"])

            review = Review(
                str(uuid3(NAMESPACE_OID, post["text"] + author)),
                title_id=title.uuid,
                text=post["text"],
                source_name="twitter",
                source_id=post["id"],
                timestamp=str(timestamp),
                reviewer=author,
            )
            self.publish(review)
