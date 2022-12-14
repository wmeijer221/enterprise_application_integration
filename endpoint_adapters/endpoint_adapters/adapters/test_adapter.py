import datetime

from endpoint_adapters.model.review import Review
from endpoint_adapters.adapters import APIAdapter


class TestAdapter(APIAdapter):
    """Test adapter that publishes a fake review periodically."""

    SLEEP_TIME = 1
    is_running = True

    def fetch(self):
        for title in self._list_of_titles:
            review_text = "Did enjoy this, but having read the book by Agatha Christie I can say that you should read the book instead. For a 2 hour movie it does not develop the characters or story very well but cinematography and direction is spectacular."
            review = Review(title, review_text, datetime.datetime.now(), reviewer="Edgar Allan Poe")
            self.publish(review)