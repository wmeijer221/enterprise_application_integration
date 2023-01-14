from dataclasses import dataclass

@dataclass(frozen=True)
class Actor:
    """Data object for actors."""

    uuid: str
    name: str
