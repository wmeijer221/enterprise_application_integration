from dataclasses import dataclass

@dataclass(eq=True, frozen=True)
class MetaEntity:
    """
    Generic model for meta entities related to movies/films.
    """
    
    uuid: str
    name: str
    meta_type: str
