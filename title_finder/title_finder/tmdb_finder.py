from os import getenv
import requests
import time
import logging
import datetime
import json
from uuid import uuid4, uuid1

from base.utils.http_status_code_helper import is_success_code
from base.canonical_model import Title
from base.channel_messaging import ChannelMessage, create_connection, publish_to_pubsub

from title_finder._version import NAME, VERSION

API_KEY_KEY = "TMDB_API_KEY"
SLEEP_INTERVAL_KEY = "SLEEP_INTERVAL"
TIMEOUT = 5
CHANNEL_KEY = "CHANNEL"
NEW_TITLE_OUT = "NEW_TITLE_OUT"

BASE_URL = "https://api.themoviedb.org/3/"
UNKNOWN_GENRE = "unknown"


class TMDBFinder:
    """
    Title finder that queries various movie/tv show lists 
    on The Movie DB and publishes them to the system.
    """

    endpoints = [
        ("movie", "popular"),
        ("movie", "now_playing"),
        ("movie", "top_rated"),
        ("tv", "popular"),
        ("tv", "on_the_air"),
        ("tv", "top_rated"),
    ]

    def __init__(self) -> None:
        self.api_key = getenv(API_KEY_KEY)
        self.sleep_interval = int(getenv(SLEEP_INTERVAL_KEY))
        self.known_genres = self.__build_genre_names()
        create_connection(getenv(CHANNEL_KEY))

    def start_collecting(self):
        """
        Starts collecting titles.
        """

        self.running = True

        while self.running:
            unique_titles = set()
            for endpoint in self.endpoints:
                logging.info(f"Trying with {endpoint}")
                details = self.__get_details(endpoint)
                unique_titles.update(details)
            self.__publish_new_titles(unique_titles)
            logging.info("Going to sleep...")
            time.sleep(self.sleep_interval)

    def __get_details(self, endpoint: str) -> 'list[Title]':
        """
        Loads show details from the provided endpoint.
        """

        s_endpoint = "/".join(endpoint)
        url = f'{BASE_URL}{s_endpoint}'
        params = {"api_key": self.api_key}
        try: 
            response = requests.request("GET", url, params=params, timeout=TIMEOUT)
        except requests.exceptions.Timeout as ex:
            logging.warning(f"Failed request to \"{url}\" with message {ex}")
            return []

        if not is_success_code(response.status_code):
            return []

        data = json.loads(response.text)
        movies = [Title(
            str(uuid4), 
            self.__get_title(entry), 
            endpoint[0], 
            self.__to_genres(entry)) 
        for entry in data["results"]]

        return movies

    def __get_title(self, entry: dict) -> str:
        """
        Returns the entry's title.
        """

        return entry['original_title'] \
            if "original_title" in entry else entry['original_name']

    def __build_genre_names(self) -> dict[int, str]:
        """
        Creates a mapping from genre ids to genre names.
        """

        loaded_genres = {}

        endpoints = [
            "genre/movie/list",
            "genre/tv/list"
        ]

        for endpoint in endpoints:
            url = f'{BASE_URL}{endpoint}'
            params = {"api_key": self.api_key}
            try:
                response = requests.get(url, params=params, timeout=TIMEOUT)
            except requests.exceptions.Timeout as ex:
                logging.warning(f'Failed to load genres from \"{url}\"')
            

            if not is_success_code(response.status_code):
                logging.warning(f'Failed to load genres from \"{url}\"')
                continue

            data = json.loads(response.text)
            for genre in data["genres"]:
                loaded_genres[genre["id"]] = genre["name"]
        
        return loaded_genres

    def __to_genres(self, entry: dict) -> 'tuple[str]':
        """
        Translates genre_id list to genre name list.
        """

        genre_ids = entry["genre_ids"]
        genre_names = []
        for id in genre_ids:
            genre = self.known_genres[id] \
                if id in self.known_genres else UNKNOWN_GENRE
            genre_names.append(genre)
        return tuple(genre_names)

    def __publish_new_titles(self, titles: list[Title]):
        """
        Publishes Title objects to the message channel.
        """

        queue_name = getenv(NEW_TITLE_OUT)
        for title in titles:
            message = ChannelMessage(
                str(uuid1()), str(uuid4()), "title",
                str(datetime.datetime.now()),
                NAME, VERSION, title)
            publish_to_pubsub(message, queue_name)
