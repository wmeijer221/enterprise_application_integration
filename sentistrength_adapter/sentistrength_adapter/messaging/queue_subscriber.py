from os import getenv
import logging

from sentistrength_adapter.messaging import QueueUser
from sentistrength_adapter.utils.json_helper import str_to_object


CHANNEL_NAME_KEY = "CHANNEL_NAME"
QUEUE_NAME_KEY = "IN_QUEUE_NAME"
EXCHANGE_NAME_KEY = "IN_EXCHANGE_NAME"


class QueueSubscriber(QueueUser):

    def __init__(self, message_type: type, on_message_received: callable):
        self.message_type = message_type
        self.on_message_received = on_message_received
        channel_name = getenv(CHANNEL_NAME_KEY)
        self.connection = self._try_connect(channel_name)
        self.channel = self.connection.channel()
        self.queue_name = getenv(QUEUE_NAME_KEY)
        self.channel.queue_declare(queue=self.queue_name)
        self.exchange = getenv(EXCHANGE_NAME_KEY, default="")
        logging.debug(
            f"Initialized queue subscriber with: {channel_name=}, queue_name={self.queue_name}, exchange={self.exchange}"
        )
        self.channel.basic_consume(
            queue=self.queue_name,
            on_message_callback=self.__handle_message,
            auto_ack=True,
        )
    
    def start(self):
        self.channel.start_consuming()

    def __handle_message(self, channel, method, properties, body):
        """Decodes message and passes it to listener."""
        json_string = body.decode('utf-8')
        message = str_to_object(json_string)
        logging.debug(f"Received message: {message.uuid}.")
        self.on_message_received(message)
