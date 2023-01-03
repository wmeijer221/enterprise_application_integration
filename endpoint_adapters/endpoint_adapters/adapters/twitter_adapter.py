import datetime
import logging
from os import getenv

import requests

from endpoint_adapters.model.review import Review
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

    def fetch(self):
        for title in self._list_of_titles:
            logging.debug('Searching for "%s" in twitter.', title)
            try:
                # Fetch tweets for title.
                posts = self.__find_posts(title)

                print(posts[0])
            except Exception as exception:
                logging.error(
                    'Error while searching for "%s" in tweets: %s.',
                    title,
                    exception.response,
                )
                continue

            logging.debug('Found %s tweets for "%s".', len(posts), title)

            self.__publish_posts(title, posts)

    def __find_posts(self, title: str) -> "list[TwitterMessage]":
        response = requests.get(
            "https://api.twitter.com/2/tweets/search/recent",
            auth=bearer_oauth,
            # All fields can be found here: https://developer.twitter.com/en/docs/twitter-api/fields
            params={
                "query": title,
                "max_results": 10,
                "tweet.fields": "id,text,edit_history_tweet_ids,author_id,created_at,lang,public_metrics,possibly_sensitive",
                "user.fields": "id,name,username,location,verified,public_metrics",
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

    def __publish_posts(self, title: str, posts: "list[TwitterMessage]"):
        """Publishes the reviews to the message queue."""
        logging.debug("Publishing %s posts to message queue.", len(posts))
        for post in posts:
            timestamp = datetime.datetime.fromisoformat(post["created_at"][0:19])
            review = Review(
                # TODO: Discuss what to do with the title.
                title="",
                message_text=post["text"],
                source_name="twitter",
                source_id=post["id"],
                timestamp=timestamp,
                reviewer=str(post["user"]["name"]),
            )
            self.publish(review)