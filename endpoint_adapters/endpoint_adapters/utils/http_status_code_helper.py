# TODO: remove this class; its duplicated in the base package.
import math

def is_success_code(status_code: int) -> bool:
    """Returns true if the status code is a success code."""
    return math.floor(status_code / 100) == 2
