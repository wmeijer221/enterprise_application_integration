import time
from socket import gaierror
import pika
import logging


class QueueUser:
    """Implements generic Queue behaviour."""
    MAX_RETRIES = 5
    TIMEOUT = 10

    def _try_connect(self, channel_name: str):
        """Implements connecting with retry-circuit breaker pattern."""
        for tries in range(1, self.MAX_RETRIES + 1):
            try:
                connection = pika.BlockingConnection(
                    pika.ConnectionParameters(host=channel_name)
                )
                return connection
            except (gaierror, pika.exceptions.AMQPConnectionError):
                logging.error("Could not connect with channel %s for the %s/%s time. Retrying in %s seconds.",
                              channel_name, tries, self.MAX_RETRIES, self.TIMEOUT)
                if tries >= self.MAX_RETRIES:
                    raise
                time.sleep(self.TIMEOUT)
        raise Exception("Illegal state; this should not be reached.")
