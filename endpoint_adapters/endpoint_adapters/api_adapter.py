import logging

from endpoint_adapters.adapters.reddit_adapter import RedditAdapter


class APIAdapter:
    def __init__(self):
        logging.info("I'm working!")
        # TODO: implement proper generic behaviour here (https://trello.com/c/hD3RPjNq/17-implement-generic-api-adapter-behaviour).
        adapter = RedditAdapter(self.publish)
        adapter.set_list_of_titles(["Breaking Bad"])
        adapter.fetch()

    def publish(self, message):
        # TODO: publish message to channel (https://trello.com/c/hD3RPjNq/17-implement-generic-api-adapter-behaviour).
        logging.info("Sending message: %s", message)
