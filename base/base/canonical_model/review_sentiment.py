from dataclasses import dataclass

@dataclass
class ReviewSentiment:
    review_uuid: str
    positivity: int = 0
    negativity: int = 0
    polarity: int = 0
    