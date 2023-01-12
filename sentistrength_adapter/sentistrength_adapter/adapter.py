import nltk
from os import getenv

from base.canonical_model.review import Review
from base.canonical_model.review_sentiment import ReviewSentiment
from base.channel_messaging import ChannelMessage, create_connection, receive_from_pubsub, publish_to_queue
from sentistrength_adapter._version import NAME, VERSION
from sentistrength_adapter.wrapper import Sentiment
from sentistrength_adapter.wrapper import SentistrengthWrapper


MESSAGE_TYPE = "sentiment"

CHANNEL_NAME_KEY = "CHANNEL_NAME"
NEW_REVIEW_IN_KEY = "NEW_REVIEW_IN"
NEW_SENTIMENT_OUT_KEY = "NEW_SENTIMENT_OUT"

class SentistrengthAdapter():
    """Adapter object that reads messages from channel and processes them through the wrapper."""

    def __init__(self, wrapper: SentistrengthWrapper):
        self.wrapper = wrapper
        channel_name = getenv(CHANNEL_NAME_KEY)
        create_connection(channel_name)
        self.new_sentiment_out = getenv(NEW_SENTIMENT_OUT_KEY)
        new_review_in = getenv(NEW_REVIEW_IN_KEY)
        receive_from_pubsub(new_review_in, self.on_message_received)

    def on_message_received(self, message: ChannelMessage):
        """Listener for new queue publisher messages."""
        sentiment = self.__build_sentiment(message.body)
        sentiment_message = ChannelMessage.channel_message_from(
            message_type=MESSAGE_TYPE,
            sender_type=NAME,
            sender_version=VERSION,
            body=sentiment
        )
        publish_to_queue(sentiment_message, self.new_sentiment_out)
    
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
