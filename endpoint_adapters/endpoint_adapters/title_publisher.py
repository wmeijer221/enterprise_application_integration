from endpoint_adapters.adapters import APIAdapter


class TitlePublisher:
    """Reads incoming titles and publishes them to the adapter."""

    # TODO: https://trello.com/c/cfROzybd/18-implement-service-for-exploring-considered-movies

    DATA_PATH = "./data/movies.txt"

    def __init__(self, receiver: APIAdapter):
        self.receiver = receiver

    def start(self):
        with open(self.DATA_PATH, "r", encoding="utf-8") as data_file:
            titles = [title.strip() for title in data_file.readlines()]
            self.receiver.set_list_of_titles(titles)
            self.receiver.fetch()
