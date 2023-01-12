"""Implements base class for the concrete adapter implementations."""

from os import getenv
from datetime import datetime

from base.canonical_model import Title

QUERY_INTERVAL_KEY = "QUERY_INTERVAL"

# TODO: Adapters now rely wholely on some other system calling ``fetch``. If that doesn't happen, new reviews are never loaded.
# TODO: Titles that adapters can find any data for, aren't ignored on consecutive runs.

class APIAdapter:
    """Base class for concrete adapter implementations."""

    _list_of_titles: set = set()
    __previous_query_time: dict[Title, datetime] = {}

    def __init__(self, publish: callable):
        self.publish = publish
        self.query_interval = int(getenv(QUERY_INTERVAL_KEY))

    def add_new_title(self, title: Title):
        self._list_of_titles.add(title)

    def fetch(self):
        """
        Called to start fetching data.
        Calls to fetch all titles that have not 
        been recently updated.
        """
        now = datetime.now()
        for title in self._list_of_titles:
            prev_query_time = self.__previous_query_time[title] if \
                title in self.__previous_query_time else datetime(1, 1, 1)
            delta = now - prev_query_time
            if delta.seconds >= self.query_interval:
                self.fetch_title(title)
                self.__previous_query_time[title] = now
            

    def fetch_title(self, title: Title):
        """Called to fetch data for a specific title."""