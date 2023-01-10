from os import getenv
import logging

from base.canonical_model.review import Review
from base.channel_messaging import ChannelMessage, create_connection, publish_to_pubsub
from endpoint_adapters._version import NAME, VERSION
from endpoint_adapters.adapters import APIAdapter, get_adapter_of_type
from endpoint_adapters.title_broker import TitleBroker


ENDPOINT_TYPE_KEY = "ENDPOINT_TYPE"
CHANNEL_NAME_KEY = "CHANNEL_NAME"
NEW_REVIEW_OUT_KEY = "NEW_REVIEW_OUT"
REVIEW_MESSAGE_TYPE = "review"


class EndpointAdapter:
    def __init__(self):
        channel_name = getenv(CHANNEL_NAME_KEY)
        self.queue_name = getenv(NEW_REVIEW_OUT_KEY)
        create_connection(channel_name)
        self.adapter, self.adapter_type = self.__build_api_adapter()
        self.title_broker = TitleBroker(self.adapter)

    def publish_review(self, review: Review):
        """Publishes a review message to the channel."""
        logging.info(f"Publishing new review: {review.uuid}.")
        message = ChannelMessage.channel_message_from(
            sender_type=f"{NAME}:{self.adapter_type}",
            message_type=REVIEW_MESSAGE_TYPE,
            sender_version=VERSION,
            body=review)
        publish_to_pubsub(message, self.queue_name)

    def __build_api_adapter(self) -> "tuple[APIAdapter, str]":
        """
        Factory method that loads an API adapter based
        on the set environment variable.
        """
        endpoint_type = getenv(ENDPOINT_TYPE_KEY).lower()
        logging.info(f"Starting API Adapter of type: {endpoint_type}.")
        try:
            adapter = get_adapter_of_type(endpoint_type, self.publish_review)
        except Exception:
            logging.critical(f"Failed to start API adapter of type: {endpoint_type}.")
            raise
        return adapter, endpoint_type
