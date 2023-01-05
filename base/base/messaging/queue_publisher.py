from os import getenv
import logging

from base.messaging.channel_message import ChannelMessage
from base.utils.json_helper import to_json
from base.messaging import QueueUser


CHANNEL_NAME_KEY = "CHANNEL_NAME"
QUEUE_NAME_KEY = "OUT_QUEUE_NAME"
EXCHANGE_NAME_KEY = "OUT_EXCHANGE_NAME"


class QueuePublisher(QueueUser):
    """Generic interface to publish to a message queue."""

    def __init__(self):
        # TODO: make env keys a constructor argument; for flexibility.
        channel_name = getenv(CHANNEL_NAME_KEY)
        self.connection = self._try_connect(channel_name)
        self.channel = self.connection.channel()
        self.queue_name = getenv(QUEUE_NAME_KEY)
        self.channel.queue_declare(queue=self.queue_name)
        self.exchange = getenv(EXCHANGE_NAME_KEY, default="")
        logging.debug(
            f"Initialized queue publisher with: {channel_name=}, queue_name={self.queue_name}, exchange={self.exchange}"
        )

    def publish(self, message: ChannelMessage):
        """Publishes the message to the channel."""
        logging.debug(f"Publishing new channel message: {message.uuid}")
        json_message = to_json(message)
        self.channel.basic_publish(
            exchange=self.exchange,
            routing_key=self.queue_name,
            body=json_message,
        )
        