from sentistrength_adapter.model.review import Review
from sentistrength_adapter.model.sentiment import Sentiment


class ReviewSentiment:
    def __init__(self, review: Review):
        self.review_uuid = review.uuid
        self.sentiment = Sentiment(0, 0, 0)

    def append(self, sentiment: Sentiment):
        self.sentiment.positivity += sentiment.positivity
        self.sentiment.negativity += sentiment.negativity
        self.sentiment.polarity += sentiment.polarity
