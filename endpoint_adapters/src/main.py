from adapters.imdb_adapter import IMDbAdapter


class main():
    def __init__(self):
        # TODO: implement proper generic behaviour here.
        adapter = IMDbAdapter(self.publish)
        adapter.fetch()

    def publish(self, message):
        # TODO: publish message to channel.
        pass


if __name__ == "__main__":
    print("hello world")
    main()
