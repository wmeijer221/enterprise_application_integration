from adapters.base_adapter import AbstractAdapter


class IMDbAdapter(AbstractAdapter):

    def fetch(self):
        print("IMDB Fetching!")
        self.publish("some message")