from os import getenv
import requests
import time
import logging
import json
from uuid import uuid4
from dataclasses import dataclass

from base.utils.http_status_code_helper import is_success_code
from base.messaging import ChannelMessage, QueuePublisher

API_KEY_KEY = "API_KEY"
SLEEP_INTERVAL_KEY = "SLEEP_INTERVAL"
TIMEOUT = 5

BASE_URL = "https://api.themoviedb.org/3/"
UNKNOWN_GENRE = "unknown"

@dataclass(eq=True, frozen=True)
class Title:
    title: str
    uuid: str
    genres: tuple[str]


class SimpleTitleFinder:
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
        self.known_genres = self.build_genre_names()
        # self.publisher = QueuePublisher()
        self.start_collecting()

    def start_collecting(self):
        self.running = True

        while self.running:
            unique_titles = set()
            for endpoint in self.endpoints:
                logging.info(f"Trying with {endpoint}")
                details = self.get_movie_details(endpoint)
                unique_titles.update(details)
            self.publish_new_titles(unique_titles)
            logging.info("Going to sleep...")
            time.sleep(self.sleep_interval)

    def get_movie_details(self, endpoint: str) -> 'list[Title]':
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
            self.get_title(entry), 
            str(uuid4()), 
            self.to_genres(entry['genre_ids'])) 
        for entry in data['results']]

        return movies


    def get_title(self, entry: dict) -> str:
        return entry['original_title'] \
            if "original_title" in entry else entry['original_name']

    def build_genre_names(self) -> dict[int, str]:
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

    def to_genres(self, genre_ids: 'list[int]') -> 'tuple[str]':
        genre_names = []
        for id in genre_ids:
            genre = self.known_genres[id] \
                if id in self.known_genres else UNKNOWN_GENRE
            genre_names.append(genre)
        return tuple(genre_names)

    def publish_new_titles(self, titles: list):
        logging.info([str(title) for title in titles])
        for title in titles:
            # TODO: This; fix the queue publisher flexibility todo note as well.
            pass
