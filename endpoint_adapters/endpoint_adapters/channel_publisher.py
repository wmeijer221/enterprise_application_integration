import logging

from endpoint_adapters.model.channel_message import ChannelMessage

from endpoint_adapters.utils.json_helper import to_json


class ChannelPublisher:
    def __init__(self):
        pass

    def publish(self, message: ChannelMessage):
        logging.info(f'Publishing new channel message: {message.uuid}')
        json_message = to_json(message)
        
        logging.info(json_message)