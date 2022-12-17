import nltk

from sentistrength_adapter._version import VERSION
from sentistrength_adapter.canonical_model.review import Review
from sentistrength_adapter.canonical_model.review_sentiment import ReviewSentiment
from sentistrength_adapter.messaging import QueuePublisher, QueueSubscriber
from sentistrength_adapter.messaging.channel_message import ChannelMessage
from sentistrength_adapter.wrapper import Sentiment
from sentistrength_adapter.wrapper import SentistrengthWrapper


MESSAGE_TYPE = "sentiment"


class SentistrengthAdapter():
    """Adapter object that reads messages from channel and processes them through the wrapper."""

    def __init__(self, wrapper: SentistrengthWrapper):
        self.wrapper = wrapper
        self.publisher = QueuePublisher()
        self.subscriber = QueueSubscriber(
            message_type=Review, on_message_received=self.on_message_received)
        self.publisher.publish(ChannelMessage({}, "asdf", "0.2.1"))
        self.subscriber.start()

    def on_message_received(self, message: ChannelMessage):
        """Listener for new queue publisher messages."""
        sentiment = self.__build_sentiment(message.body)
        sentiment_message = ChannelMessage(sentiment, MESSAGE_TYPE, VERSION)
        self.publisher.publish(sentiment_message)
    
    def __build_sentiment(self, review: Review) -> ReviewSentiment:
        """Factory method for review sentiment"""
        review_sentiment = ReviewSentiment(review.uuid)
        # NOTE: this assumes the text is english.
        sentences = nltk.sent_tokenize(review.text)
        for sentence in sentences:
            sentiment = self.wrapper.get_sentiment(sentence)
            review_sentiment = self.__append_sentiment(review_sentiment, sentiment)
        return review_sentiment

    def __append_sentiment(self, review_sentiment: ReviewSentiment, sentiment: Sentiment) -> ReviewSentiment:
        # TODO: This could be more sophisticated.
        review_sentiment.positivity += sentiment.positivity
        review_sentiment.negativity += sentiment.negativity
        review_sentiment.polarity += sentiment.polarity
        return review_sentiment
