import logging

from dotenv import load_dotenv

from adapters.reddit_adapter import RedditAdapter


class main():
    def __init__(self):
        # TODO: implement proper generic behaviour here (https://trello.com/c/hD3RPjNq/17-implement-generic-api-adapter-behaviour).
        adapter = RedditAdapter(self.publish)
        adapter.set_list_of_titles(["Breaking Bad"])
        adapter.fetch()

    def publish(self, message):
        # TODO: publish message to channel (https://trello.com/c/hD3RPjNq/17-implement-generic-api-adapter-behaviour).
        print(f'Sending message: {message}')


if __name__ == "__main__":
    print("hello world")
    logging.basicConfig(level=logging.INFO)
    load_dotenv()
    main()
