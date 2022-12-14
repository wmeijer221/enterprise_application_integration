import datetime
from uuid import uuid4


class Review:
    """Data object for reviews."""

    def __init__(
        self,
        title: str,
        message_text: str,
        timestamp: datetime.datetime,
        reviewer: str,
    ):
        self.uuid = str(uuid4())
        self.title = title
        self.timestamp = str(timestamp)
        self.reviewer = reviewer
        self.text = message_text
