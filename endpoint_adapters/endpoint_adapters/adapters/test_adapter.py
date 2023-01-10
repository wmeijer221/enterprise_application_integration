import datetime
import logging
from uuid import uuid4

from base.canonical_model import Review, Title

from endpoint_adapters.adapters import APIAdapter

class TestAdapter(APIAdapter):
    """Test adapter that publishes a fake review periodically."""

    review_id: int = 0

    def fetch_title(self, title: Title):
        logging.info(title)
        review_text = f"Did enjoy this, but having read the book by Agatha Christie I can say that you should read the book instead. For a 2 hour movie it does not develop the characters or story very well but cinematography and direction is spectacular."
        review = Review(
            str(uuid4()),
            title.uuid,
            review_text,
            source_name="test",
            source_id=self.review_id,
            timestamp=str(datetime.datetime.now()),
            reviewer="Edgar Allan Poe",
        )
        self.review_id += 1
        self.publish(review)
