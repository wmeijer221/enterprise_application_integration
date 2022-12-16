import datetime

from endpoint_adapters.model.review import Review
from endpoint_adapters.adapters import APIAdapter


class TestAdapter(APIAdapter):
    """Test adapter that publishes a fake review periodically."""

    def fetch(self):
        for index, title in enumerate(self._list_of_titles):
            review_text = f"Did enjoy this, but having read the book by Agatha Christie I can say that you should read the book instead. For a 2 hour movie it does not develop the characters or story very well but cinematography and direction is spectacular."
            review = Review(
                title,
                review_text,
                source_name="test",
                source_id=index,
                timestamp=datetime.datetime.now(),
                reviewer="Edgar Allan Poe",
            )
            self.publish(review)
