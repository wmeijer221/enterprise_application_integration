from os import getenv

from base.channel_messaging import ChannelMessage, receive_from_pubsub
from base.canonical_model import Title
from endpoint_adapters.adapters import APIAdapter

NEW_TITLE_IN = "NEW_TITLE_IN"

class TitleBroker:
    """Reads incoming titles and publishes them to the adapter."""

    running = True

    def __init__(self, receiver: APIAdapter):
        self.receiver = receiver
        queue_name = getenv(NEW_TITLE_IN)
        receive_from_pubsub(queue_name, self.__on_title_received)

    def __on_title_received(self, message: ChannelMessage):
        title: Title = message.body
        self.receiver.add_new_title(title)
        self.receiver.fetch()
