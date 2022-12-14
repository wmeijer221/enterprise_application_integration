"""Implements base class for the concrete adapter implementations."""


class AbstractAdapter:
    """Base class for concrete adapter implementations."""

    def __init__(self, publish: callable):
        self.publish = publish

    def fetch(self):
        """Called to start fetching data."""
