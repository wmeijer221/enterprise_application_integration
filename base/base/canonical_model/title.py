from dataclasses import dataclass
from typing import Sequence

@dataclass(eq=True, frozen=True)
class Title:
    """
    Generic model for meta entities related to movies/films.
    """
    
    uuid: str 
    name: str # the name of the title
    type: str # e.g. tv show vs. movie
    genres: tuple[str]

    def __init__(self, uuid: str, name: str, type: str, 
                 genres: Sequence[str]):
        object.__setattr__(self, "uuid", uuid)
        object.__setattr__(self, "name", name)
        object.__setattr__(self, "type", type)
        if not isinstance(genres, tuple):
           genres = tuple(genres)
        object.__setattr__(self, "genres", genres)
