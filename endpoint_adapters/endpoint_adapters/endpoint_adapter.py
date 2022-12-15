from os import getenv
import logging

from endpoint_adapters.title_broker import TitleBroker
from endpoint_adapters.queue_publisher import QueuePublisher
from endpoint_adapters.adapters import APIAdapter, get_adapter_of_type
from endpoint_adapters.model.channel_message import ChannelMessage
from endpoint_adapters.model.review import Review

from endpoint_adapters._version import VERSION

ENDPOINT_TYPE_KEY = "ENDPOINT_TYPE"
REVIEW_MESSAGE_TYPE = "review"


class EndpointAdapter:
    def __init__(self):
        self.channel_publisher = QueuePublisher()
        self.adapter, self.adapter_type = self.__build_api_adapter()
        self.title_broker = TitleBroker(self.adapter)
        self.title_broker.start()

    def publish_review(self, review: Review):
        """Publishes a review message to the channel."""
        logging.info(f"Publishing new review: {review.uuid}.")
        message = ChannelMessage(
            review,
            message_type=REVIEW_MESSAGE_TYPE,
            adapter_version=VERSION,
        )
        self.channel_publisher.publish(message)

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
