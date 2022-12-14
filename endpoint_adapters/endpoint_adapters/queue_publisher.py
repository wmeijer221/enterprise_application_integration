from os import getenv

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

    def __init__(self):
        channel_name = getenv(CHANNEL_NAME_KEY)
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=channel_name)
        )
        self.channel = self.connection.channel()
        queue_name = getenv(QUEUE_NAME_KEY)
        self.channel.queue_declare(queue=queue_name)
        self.exchange = getenv(EXCHANGE_NAME_KEY, default="")
        self.routing_key = getenv(ROUTING_KEY_KEY, default="")
        logging.info(
            f"Initialized queue publisher with: {channel_name=}, {queue_name=}, routing_key={self.routing_key}, exchange={self.exchange}"
        )

    def publish(self, message: ChannelMessage):
        """Publishes the message to the channel."""
        logging.info(f"Publishing new channel message: {message.uuid}")
        json_message = to_json(message)
        self.channel.basic_publish(
            exchange=self.exchange,
            routing_key=self.routing_key,
            body=json_message,
        )
