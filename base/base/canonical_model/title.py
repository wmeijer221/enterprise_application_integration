from dataclasses import dataclass

@dataclass(eq=True, frozen=True)
class Title:
    """
    Generic model for meta entities related to movies/films.
    """
    
    uuid: str 
    name: str # the name of the title
    type: str # e.g. tv show vs. movie
    genres: tuple[str]
