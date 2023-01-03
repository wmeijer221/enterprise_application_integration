from os import getenv
import time
from socket import gaierror
import logging
import pika

RABBIT_MQ_HOST_KEY = "RABBIT_MQ_HOST"
LOGGER = logging.getLogger(__name__)
ASYNC = False
QUEUES = ['new_review']

class QueueConsumer:
    """Generic interface to consume message queues."""

    MAX_RETRIES = 5
    TIMEOUT = 10

    def __init__(self):
        rabbit_mq_host = getenv(RABBIT_MQ_HOST_KEY)
        self.connection = self.__try_connect(rabbit_mq_host)
        if not ASYNC:
            self.channel = self.connection.channel()
        LOGGER.debug(
            f"Initialized queue consumer with: {rabbit_mq_host=}"
        )

    def __async_new_review_callback(self, channel, method, properties, body):
        LOGGER.debug("New review!")
        LOGGER.debug(body)

    def __async_on_channel_open(self, channel):
        LOGGER.debug("__on_open callback called! Channel opened")
        self.channel = channel
        self.channel.basic_consume(queue='new_review', on_message_callback=self.__async_new_review_callback, auto_ack=True)
        # for queue in QUEUES:
            # self.channel.basic_consume(queue=queue, on_message_callback=self.__async_new_review_callback, auto_ack=True)

    def __async_on_connection_open(self, connection):
        LOGGER.debug("__on_open callback called! Connection opened")
        connection.channel(on_open_callback=self.__async_on_channel_open)

    def __try_connect(self, rabbit_mq_host: str):
        """Implements connecting with retry-circuit breaker pattern."""
        if ASYNC:
            for tries in range(1, self.MAX_RETRIES + 1):
                connection = pika.SelectConnection(
                    parameters=pika.ConnectionParameters(host=rabbit_mq_host),
                    on_open_callback=self.__async_on_connection_open
                )
                try:
                        connection.ioloop.start()
                except gaierror:
                    LOGGER.error("Could not connect with channel %s for the %s/%s time. Retrying in %s seconds.", rabbit_mq_host, tries, self.MAX_RETRIES, self.TIMEOUT)
                    if tries >= self.MAX_RETRIES:
                        raise
                    time.sleep(self.TIMEOUT)
                except KeyboardInterrupt:
                    # Gracefully close the connection
                    connection.close()
                    # Start the IOLoop again so Pika can communicate, it will stop on its own when the connection is closed
                    connection.ioloop.start()
            raise Exception("Illegal state; this should not be reached.")
        else:
            for tries in range(1, self.MAX_RETRIES + 1):
                try:
                    connection = pika.BlockingConnection(
                        pika.ConnectionParameters(host=rabbit_mq_host)
                    )
                    return connection
                except gaierror:
                    LOGGER.error("Could not connect with channel %s for the %s/%s time. Retrying in %s seconds.", rabbit_mq_host, tries, self.MAX_RETRIES, self.TIMEOUT)
                    if tries >= self.MAX_RETRIES:
                        raise
                    time.sleep(self.TIMEOUT)
        raise Exception("Illegal state; this should not be reached.")

    def add_queue_consumer(self, queue, on_message_callback):
        LOGGER.debug(f"Starting to consume queue {queue} with callback {on_message_callback}")
        self.channel.basic_consume(queue=queue, on_message_callback=on_message_callback, auto_ack=True)

    def start_consuming(self):
        try:
            self.channel.start_consuming()
        except KeyboardInterrupt:
            self.channel.stop_consuming()
