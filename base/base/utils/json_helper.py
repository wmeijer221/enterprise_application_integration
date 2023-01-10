import json
from collections import namedtuple

def to_json(obj: object) -> str:
    """Transforms the object to a json string"""
    return json.dumps(obj, default=lambda x: x.__dict__)

def str_to_object(json_object: str) -> object: 
    result = json.loads(json_object, object_hook=_json_object_hook)
    return result

def _json_object_hook(data: dict) -> object: 
    result = namedtuple('X', data.keys())(*data.values())
    return result
    