from os import getenv
import logging

from sentistrength_adapter.messaging import QueueUser

CHANNEL_NAME_KEY = "CHANNEL_NAME"
QUEUE_NAME_KEY = "OUT_QUEUE_NAME"
EXCHANGE_NAME_KEY = "OUT_EXCHANGE_NAME"


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

        # Consume the RabbitMQ queue
        self.channel.basic_consume(
            queue="hello",
            on_message_callback=self.handle_message,
            auto_ack=True,
        )

    def handle_message(self, ch, method, properties, body):
        print(ch)
        print(method)
        print(properties)
        print(body)
