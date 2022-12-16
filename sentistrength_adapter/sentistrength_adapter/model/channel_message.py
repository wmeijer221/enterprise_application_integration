import datetime
from uuid import uuid1, uuid4


class ChannelMessage:
    """Data object for review messages."""

    def __init__(
        self, body: object, message_type: str, adapter_version: str
    ):
        self.host_uuid = str(uuid1())
        self.uuid = str(uuid4())
        self.message_type = message_type
        self.timestamp = str(datetime.datetime.now())
        self.adapter_version = adapter_version
        self.body = body