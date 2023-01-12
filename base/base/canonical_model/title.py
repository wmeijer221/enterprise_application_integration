from dataclasses import dataclass
from typing import Sequence

from base.utils.obj_helper import ensure_tuple

@dataclass(eq=True, frozen=True)
class Title:
    """
    Generic model for meta entities related to movies/films.
    """
    
    uuid: str 
    name: str # the name of the title
    type: str # e.g. tv show vs. movie
    genres: tuple[str]
    cast: tuple[str]
    crew: tuple[str]

    def __init__(self, uuid: str, name: str, type: str, 
                 genres: Sequence[str], cast: Sequence[str], 
                 crew: Sequence[str]):
        object.__setattr__(self, "uuid", uuid)
        object.__setattr__(self, "name", name)
        object.__setattr__(self, "type", type)
        object.__setattr__(self, "genres", ensure_tuple(genres))
        object.__setattr__(self, "cast", ensure_tuple(cast))
        object.__setattr__(self, "crew", ensure_tuple(crew))
