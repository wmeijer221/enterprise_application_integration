
class Sentiment():
    """Container object for sentiment"""

    def __init__(self, text: str, positivity: int, negativity: int, polarity: int):
        self.text = text
        self.positive = positivity
        self.negative = negativity
        self.polarity = polarity

    def __str__(self) -> str:
        return f'{self.text=}, {self.polarity=}, {self.positive=}, {self.negative=}'
        