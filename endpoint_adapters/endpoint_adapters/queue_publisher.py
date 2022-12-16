from os import getenv
import time
from socket import gaierror
import logging
import pika


from endpoint_adapters.model.channel_message import ChannelMessage
from endpoint_adapters.utils.json_helper import to_json

CHANNEL_NAME_KEY = "CHANNEL_NAME"
QUEUE_NAME_KEY = "QUEUE_NAME"
EXCHANGE_NAME_KEY = "EXCHANGE_NAME"
ROUTING_KEY_KEY = "ROUTING_KEY"


class QueuePublisher:
    """Generic interface to publish to a message queue."""

    MAX_RETRIES = 5
    TIMEOUT = 10

    def __init__(self):
        channel_name = getenv(CHANNEL_NAME_KEY)
        self.connection = self.__try_connect(channel_name)
        self.channel = self.connection.channel()
        self.queue_name = getenv(QUEUE_NAME_KEY)
        self.channel.queue_declare(queue=self.queue_name)
        self.exchange = getenv(EXCHANGE_NAME_KEY, default="")
        logging.info(
            f"Initialized queue publisher with: {channel_name=}, queue_name={self.queue_name}, exchange={self.exchange}"
        )

    def __try_connect(self, channel_name: str):
        """Implements connecting with retry-circuit breaker pattern."""
        for tries in range(1, self.MAX_RETRIES + 1):
            try:
                connection = pika.BlockingConnection(
                    pika.ConnectionParameters(host=channel_name)
                )
                return connection
            except gaierror:
                logging.error("Could not connect with channel %s for the %s/%s time. Retrying in %s seconds.", channel_name, tries, self.MAX_RETRIES, self.TIMEOUT)
                if tries >= self.MAX_RETRIES:
                    raise
                time.sleep(self.TIMEOUT)
        raise Exception("Illegal state; this should not be reached.")

    def publish(self, message: ChannelMessage):
        """Publishes the message to the channel."""
        logging.info(f"Publishing new channel message: {message.uuid}")
        json_message = to_json(message)
        self.channel.basic_publish(
            exchange=self.exchange,
            routing_key=self.queue_name,
            body=json_message,
        )