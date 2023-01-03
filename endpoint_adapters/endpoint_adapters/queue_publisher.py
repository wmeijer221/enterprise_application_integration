from os import getenv
import time
from socket import gaierror
import logging
import pika
import json


from endpoint_adapters.model.channel_message import ChannelMessage
from endpoint_adapters.utils.json_helper import to_json

CHANNEL_NAME_KEY = "CHANNEL_NAME"
# QUEUE_NAME_KEY = "QUEUE_NAME"
QUEUE_NAMES_KEY = "QUEUE_NAMES"
EXCHANGE_NAME_KEY = "EXCHANGE_NAME"


class QueuePublisher:
    """Generic interface to publish to a message queue."""

    MAX_RETRIES = 5
    TIMEOUT = 10

    def __init__(self):
        channel_name = getenv(CHANNEL_NAME_KEY)
        self.connection = self.__try_connect(channel_name)
        self.channel = self.connection.channel()
        # self.queue_name = getenv(QUEUE_NAMES_KEY)
        self.queue_names = json.loads(getenv(QUEUE_NAMES_KEY))
        for queue_name in self.queue_names:
            self.channel.queue_declare(queue=queue_name)
        self.exchange = getenv(EXCHANGE_NAME_KEY, default="")
        logging.debug(
            f"Initialized queue publisher with: {channel_name=}, queue_names={json.dumps(self.queue_names)}, exchange={self.exchange}"
        )

    def __try_connect(self, channel_name: str):
        """Implements connecting with retry-circuit breaker pattern."""
        for tries in range(1, self.MAX_RETRIES + 1):
            try:
                connection = pika.BlockingConnection(
                    pika.ConnectionParameters(host=channel_name)
                )
                return connection
            except (gaierror, pika.exceptions.AMQPConnectionError):
                logging.error("Could not connect with channel %s for the %s/%s time. Retrying in %s seconds.", channel_name, tries, self.MAX_RETRIES, self.TIMEOUT)
                if tries >= self.MAX_RETRIES:
                    raise
                time.sleep(self.TIMEOUT)
        raise Exception("Illegal state; this should not be reached.")

    def publish(self, message: ChannelMessage):
        """Publishes the message to the channel."""
        logging.debug(f"Publishing new channel message: {message.uuid}")
        json_message = to_json(message)
        for queue_name in self.queue_names:
            self.channel.basic_publish(
                exchange=self.exchange,
                routing_key=queue_name,
                body=json_message,
            )
