
class Sentiment():
    """Container object for sentiment"""

    def __init__(self, text: str, positivity: int, negativity: int, classification: int):
        self.text = text
        self.positivity = positivity
        self.negativity = negativity
        self.polarity = classification

    def __str__(self) -> str:
        return f'{self.text=}, {self.polarity=}, {self.positivity=}, {self.negativity=}'
