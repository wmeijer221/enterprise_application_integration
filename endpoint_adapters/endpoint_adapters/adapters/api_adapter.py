"""Implements base class for the concrete adapter implementations."""

from base.canonical_model import Title

class APIAdapter:
    """Base class for concrete adapter implementations."""

    _list_of_titles: "list[Title]" = []

    def __init__(self, publish: callable):
        self.publish = publish

    def set_list_of_titles(self, list_of_titles: "list[Title]"):
        """Setter for list of titles."""
        self._list_of_titles = list_of_titles

    def add_new_title(self, title: Title):
        self._list_of_titles.append(title)

    def fetch(self):
        """Called to start fetching data."""
