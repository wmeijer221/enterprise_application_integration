import nltk

from sentistrength_adapter.wrapper import SentistrengthWrapper
from sentistrength_adapter.messaging import QueuePublisher, QueueSubscriber
from sentistrength_adapter.model.channel_message import ChannelMessage
from sentistrength_adapter.model.review import Review
from sentistrength_adapter.model.review_sentiment import ReviewSentiment
from sentistrength_adapter._version import VERSION

MESSAGE_TYPE = "sentiment"


class SentistrengthAdapter():
    """Adapter object that reads messages from channel and processes them through the wrapper."""

    def __init__(self, wrapper: SentistrengthWrapper):
        self.wrapper = wrapper
        self.publisher = QueuePublisher()
        self.subscriber = QueueSubscriber(
            message_type=Review, on_message_received=self.on_message_received)

    def on_message_received(self, message: ChannelMessage):
        """Listener for new queue publisher messages."""
        sentiment = self.__build_sentiment(message.body)
        sentiment_message = ChannelMessage(sentiment, MESSAGE_TYPE, VERSION)
        self.publisher.publish(sentiment_message)

    def __build_sentiment(self, review: Review) -> ReviewSentiment:
        """Factory method for review sentiment"""
        review_sentiment = ReviewSentiment(review)
        # NOTE: this assumes the text is english.
        sentences = nltk.sent_tokenize(review.text)
        for sentence in sentences:
            sentiment = self.wrapper.get_sentiment(sentence)
            review_sentiment.append(sentiment)
        return review_sentiment
