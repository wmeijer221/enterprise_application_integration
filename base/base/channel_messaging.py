"""
Implements basic channel communication methods for 
standard queues and standard publish-subscribe channels..
"""

from dataclasses import dataclass
import datetime
import logging
import pika
from pika.adapters.blocking_connection import BlockingConnection, BlockingChannel
from socket import gaierror
import time
from typing import Callable
from uuid import uuid1, uuid4

from base.utils.json_helper import to_json, str_to_object

@dataclass(frozen=True)
class ChannelMessage:
    """
    Data object for network messages.
    """

    host_uuid: str
    uuid: str
    message_type: str
    timestamp: str
    sender_type: str
    sender_version: str
    body: object

    @classmethod
    def channel_message_from(cls, message_type: str, sender_type: str, sender_version: str, body: object) -> 'ChannelMessage':
        """
        Factory method for constructing a ``ChannelMessage`` using default settings for IDs and datetime.
        """

        return ChannelMessage(
            str(uuid1()), 
            str(uuid4()), 
            message_type, 
            str(datetime.datetime.now()), 
            sender_type, 
            sender_version, 
            body
        )


connection: BlockingConnection = None
channel: BlockingChannel = None

known_queues = set()
queue_listeners: dict[str, callable] = {}

known_pubsubs = set()
known_pubsub_receivers = {}
pubsub_listeners: dict[str, callable] = {}

def create_connection(channel_name: str, stop_if_existing: bool = True, max_retries: int = 5, timeout: int = 10):
    """
    Creates new connection to ``channel_name``.
    If ``stop_if_existing`` is True, a connection 
    is only made if none exists yet.
    """

    global connection, channel

    if stop_if_existing and __connection_is_present():
        return

    for tries in range(1, max_retries + 1):
        try:
            connection = pika.BlockingConnection(
                pika.ConnectionParameters(host=channel_name)
            )
            channel = connection.channel()
        except (gaierror, pika.exceptions.AMQPConnectionError):
            logging.error("Could not connect with channel %s for the %s/%s time. Retrying in %s seconds.",
                            channel_name, tries, max_retries, timeout)
            if tries >= max_retries:
                raise
            time.sleep(timeout)

def __connection_is_present() -> bool:
    """
    Returns true if the connection already exists.
    """

    global connection, channel
    return 'connection' in locals() and 'channel' in locals \
        and not connection is None and not channel  is None

def publish_to_queue(message: ChannelMessage, queue_name: str, 
                     exchange_name: str = ""):
    """
    Publishes ``message`` to ``queue_name`` using ``exchange_name``.
    """

    global channel
    logging.debug(f"Publishing new channel message: {message.uuid}")
    ensure_queue_exists(queue_name)
    json_message = to_json(message)
    channel.basic_publish(
        exchange=exchange_name,
        routing_key=queue_name,
        body=json_message,
    )

def receive_from_queue(queue_name: str, on_message_callback: 'Callable[[ChannelMessage], None]'):
    """
    Adds ``on_message_callback`` as a listener to messages from ``queue_name``.
    """
    global queue_listeners, channel

    def recv_from_queue(channel, method, properties, body):
        queue_name = method.queue
        message = __body_to_message(body)
        callback = queue_listeners[queue_name]
        callback(message)

    queue_listeners[queue_name] = on_message_callback
    ensure_queue_exists(queue_name)
    channel.basic_consume(
        queue=queue_name,
        on_message_callback=recv_from_queue,
        auto_ack=True,
    )

def ensure_queue_exists(queue_name: str):
    """
    Creates queue ``queue_name`` when it is unknown to this client.
    """

    global channel
    if queue_name not in known_queues:
        channel.queue_declare(queue=queue_name)
        known_queues.add(queue_name)

def publish_to_pubsub(message: ChannelMessage, pubsub_name: str, exchange_name: str = ""):
    """
    Publishes a new message to the ``pubsub_name`` channel.
    """

    logging.debug(f"Publishing new channel message: {message.uuid}")
    ensure_pubsub_exists(pubsub_name)
    json_message = to_json(message)
    channel.basic_publish(
        exchange=pubsub_name,
        routing_key=exchange_name,
        body=json_message,
    )

def receive_from_pubsub(pubsub_name: str, on_message_callback: 'Callable[[ChannelMessage], None]'):
    """
    Creates listener for the ``pubsub_name`` channel, 
    calling ``on_message_callback`` whenever a new message arrives.
    """

    global known_pubsub_receivers, pubsub_listeners
    
    def recv_from_pubsub(channel, method, properties, body):
        exchange_name = method.exchange
        message = __body_to_message(body)
        callback = pubsub_listeners[exchange_name]
        callback(message)

    ensure_pubsub_exists(pubsub_name)
    ensure_pubsub_receiver_exists(pubsub_name)
    queue_name = known_pubsub_receivers[pubsub_name]
    pubsub_listeners[pubsub_name] = on_message_callback
    channel.basic_consume(
        queue=queue_name,
        on_message_callback=recv_from_pubsub,
        auto_ack=True
    )

    channel.start_consuming()

def ensure_pubsub_exists(pubsub_name: str, exchange_type: str = "fanout"):
    """
    Creates pubsub channel if none exists yet.
    """

    global channel, known_pubsubs
    if not pubsub_name in known_pubsubs:
        channel.exchange_declare(pubsub_name, exchange_type)

def ensure_pubsub_receiver_exists(pubsub_name: str, exclusive: bool = False):
    """
    Creates pubsub receiver channel if none exists yet.
    """

    global known_pubsub_receivers
    if not pubsub_name in known_pubsub_receivers:
        result = channel.queue_declare(queue="", exclusive=exclusive)
        queue_name = result.method.queue
        channel.queue_bind(exchange=pubsub_name, queue=queue_name)
        known_pubsub_receivers[pubsub_name] = queue_name

def __body_to_message(body: str) -> ChannelMessage:
    """
    Converts the body of a network message to a ``ChannelMessage`` object.
    """

    json_string = body.decode('utf-8')
    message = str_to_object(json_string)
    return message
    