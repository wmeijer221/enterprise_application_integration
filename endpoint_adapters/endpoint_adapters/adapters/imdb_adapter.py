"""Adapter for IMDb reviews."""

from dateutil.parser import parse as parse_date
import json
import logging
import requests
from uuid import uuid4

from base.canonical_model import Review, Title

from endpoint_adapters.adapters import APIAdapter
from endpoint_adapters.utils.http_status_code_helper import is_success_code


class IMDbAdapter(APIAdapter):
    """Adapter for IMDb reviews."""

    BASE_URL = "https://imdb-api.tprojects.workers.dev"
    TIMEOUT = 5

    def fetch_title(self, title: Title):
        release_id = self.__fetch_release_id(title.name)
        if id is None:
            logging.warning(f"Failed to load IMDB reviews for {title.name}")
            return
        reviews = self.__fetch_reviews(release_id)
        if reviews is None:
            logging.warning(f"Failed to load IMDB reviews for {title.name}")
            return
        self.__publish_reviews(title, reviews)

    def __fetch_release_id(self, title) -> str:
        """Fetches the IMDb ID for a given title."""
        logging.debug("Fetching IMDb ID for %s.", title)
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
                logging.debug("Found IMDb IDs for %s: %s.", title, release_id)
                return release_id

        logging.error("No IMDb ID found for %s.", title)
        return None

    def __fetch_reviews(self, release_id: str) -> "list[dict]":
        """Fetches the reviews for a given title."""
        logging.debug("Fetching reviews for %s.", release_id)
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
        logging.debug("Found %s reviews for %s", len(reviews), release_id)
        return reviews

    def __publish_reviews(self, title: Title, reviews: "list[dict]"):
        """Publishes the reviews to the message queue."""
        logging.debug("Publishing %s reviews to message queue.", len(reviews))
        for review in reviews:
            timestamp = parse_date(review["date"])
            real_review = Review(
                uuid=str(uuid4()),
                title_id=title.uuid,
                text=review["content"],
                source_name="imdb",
                source_id=review["id"],
                timestamp=str(timestamp),
                reviewer="author",
            )
            self.publish(real_review)
