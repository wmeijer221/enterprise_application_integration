import logging
from os import getenv
import time

from endpoint_adapters.adapters import APIAdapter


class TitleBroker:
    """Reads incoming titles and publishes them to the adapter."""

    # TODO: https://trello.com/c/cfROzybd/18-implement-service-for-exploring-considered-movies

    DATA_PATH = "./data/movies.txt"
    INTERVAL_KEY = "UPDATE_INTERVAL"
    running = True

    def __init__(self, receiver: APIAdapter):
        self.receiver = receiver

    def start(self):
        """Starts publishing new titles, and periodically updates the reviews on those."""
        with open(self.DATA_PATH, "r", encoding="utf-8") as data_file:
            titles = [title.strip() for title in data_file.readlines()]
        update_interval = int(getenv(self.INTERVAL_KEY))
        while self.running:
            self.receiver.set_list_of_titles(titles)
            self.receiver.fetch()
            logging.info("Title broker going to sleep for %s seconds...", update_interval)
            time.sleep(update_interval)
