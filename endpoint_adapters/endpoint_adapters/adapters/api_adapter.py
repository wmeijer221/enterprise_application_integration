"""Implements base class for the concrete adapter implementations."""


class APIAdapter:
    """Base class for concrete adapter implementations."""

    _list_of_titles: "list[str]"

    def __init__(self, publish: callable):
        self.publish = publish

    def set_list_of_titles(self, list_of_titles: "list[str]"):
        """Setter for list of titles."""
        self._list_of_titles = list_of_titles

    def fetch(self):
        """Called to start fetching data."""
