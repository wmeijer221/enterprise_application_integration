from dataclasses import dataclass

from base.canonical_model.review_sentiment import ReviewSentiment


@dataclass(frozen=True)
class Review:
    """Data object for reviews."""

    uuid: str
    title_id: str
    text: str
    source_name: str
    source_id: str
    timestamp: str
    reviewer: str

    sentiment: ReviewSentiment = None
