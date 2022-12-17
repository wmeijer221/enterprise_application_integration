
class ReviewSentiment:
    def __init__(self, review_uuid: str, positivity: int = 0, 
                 negativity: int = 0, polarity: int = 0):
        self.review_uuid = review_uuid
        self.positivity = positivity
        self.negativity = negativity
        self.polarity = polarity 
