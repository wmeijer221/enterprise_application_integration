import json


def to_json(obj: object) -> str:
    """Transforms the object to a json string"""
    return json.dumps(obj, default=lambda x: x.__dict__)
