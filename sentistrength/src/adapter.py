"""Implements a simple adapter for the Sentistrength JAR."""
from wrapper import SentistrengthWrapper


class SentistrengthAdapter():
    """Adapter object that reads messages from channel and processes them through the wrapper."""

    def __init__(self, wrapper: SentistrengthWrapper):
        self.is_listening = True
        self.wrapper = wrapper
        self.listen()

    def listen(self):
        while self.is_listening:
            text = self.read_incoming()
            if text is None:
                break
            sentiment = self.wrapper.get_sentiment(text)
            print(sentiment)

    documents = ['I love this', 'I hate this',
                 'this is awesome', 'what the hell man',
                 'just some stuff', 'yeah right you know what you are doing']
    index = 0

    def read_incoming(self) -> str:
        # TODO implement reading from message queue.
        if self.index >= len(self.documents):
            return None
        text = self.documents[self.index]
        self.index += 1
        return text
