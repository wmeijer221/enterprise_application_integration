import datetime
from uuid import uuid4


# TODO: update to dataclass.
class Review:
    """Data object for reviews."""

    def __init__(
        self,
        title: str,
        text: str,
        source_name: str,
        source_id: str,
        timestamp: datetime.datetime,
        reviewer: str,
    ):
        self.uuid = str(uuid4())
        self.title = title
        self.source_name = source_name
        self.source_id = source_id
        self.timestamp = str(timestamp)
        self.reviewer = reviewer
        self.text = text
