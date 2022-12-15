"""Adapter for IMDb reviews."""

from dateutil.parser import parse as parse_date
import json
import logging
import requests

from endpoint_adapters.adapters import APIAdapter
from endpoint_adapters.model.review import Review
from endpoint_adapters.utils.http_status_code_helper import is_success_code


class IMDbAdapter(APIAdapter):
    """Adapter for IMDb reviews."""

    BASE_URL = "https://imdb-api.tprojects.workers.dev"
    TIMEOUT = 5

    def fetch(self):
        release_ids = self.__fetch_release_ids(self._list_of_titles)
        logging.info(
            "Found %s IMDb IDs for %s titles.",
            len(release_ids),
            len(self._list_of_titles),
        )
        for title, release_id in zip(self._list_of_titles, release_ids):
            reviews = self.__fetch_reviews(release_id)
            if reviews is None:
                continue
            self.__publish_reviews(title, reviews)

    def __fetch_release_ids(self, titles: "list[str]") -> "list[str]":
        """Fetches the IMDb IDs for a list of titles."""
        titles = [self.__fetch_release_id(title) for title in titles]
        return [title for title in titles if title is not None]

    def __fetch_release_id(self, title) -> str:
        """Fetches the IMDb ID for a given title."""
        logging.info("Fetching IMDb ID for %s.", title)
        url = f"{self.BASE_URL}/search"
        params = {"query": title}

        try:
            response = requests.request("GET", url, params=params, timeout=self.TIMEOUT)
        except requests.exceptions.Timeout:
            logging.error("Timeout while fetching IMDb ID for %s.", title)
            return None

        if not is_success_code(response.status_code):
            logging.error("Failed to fetch IMDb ID for %s.", title)
            return None

        response_json = json.loads(response.text)

        entries = [
            {"title": release["title"], "id": release["id"]}
            for release in response_json["results"]
        ]
        # Returns exact match
        for reliease in entries:
            if reliease["title"] == title:
                release_id = reliease["id"]
                logging.info("Found IMDb IDs for %s: %s.", title, release_id)
                return release_id

        logging.error("No IMDb ID found for %s.", title)
        return None

    def __fetch_reviews(self, release_id: str) -> "list[dict]":
        """Fetches the reviews for a given title."""
        logging.info("Fetching reviews for %s.", release_id)
        url = f"{self.BASE_URL}/reviews/{release_id}"
        params = {"option": "helpfulness", "sortOrder": "descending"}

        try:
            response = requests.request("GET", url, params=params, timeout=self.TIMEOUT)
        except requests.exceptions.Timeout:
            logging.error("Timeout while fetching reviews for %s.", release_id)
            return None

        if not is_success_code(response.status_code):
            logging.error("Failed to fetch reviews for %s.", release_id)
            return None

        response_json = json.loads(response.text)
        if len(response_json) == 0:
            logging.error("No reviews found for %s.", release_id)
            return None

        reviews = list([review for review in response_json["reviews"]])
        logging.info("Found %s reviews for %s", len(reviews), release_id)
        return reviews

    def __publish_reviews(self, title: str, reviews: "list[dict]"):
        """Publishes the reviews to the message queue."""
        logging.info("Publishing %s reviews to message queue.", len(reviews))
        for review in reviews:
            timestamp = parse_date(review["date"])
            real_review = Review(
                title=title,
                message_text=review["content"],
                source_name="imdb",
                source_id=review["id"],
                timestamp=timestamp,
                reviewer="author",
            )
            self.publish(real_review)
