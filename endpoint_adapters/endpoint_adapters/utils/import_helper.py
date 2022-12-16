import importlib
from inspect import getmembers, isclass


def get_instance_of_type_from(module_type: type, module_path: str, **kwargs):
    """
    Creates an instance of the provided module type, found in the provided
    module path, initiatlized with the provided arguments
    """
    target_module = importlib.import_module(module_path)
    for _, member in getmembers(target_module):
        if (
            isclass(member)
            and issubclass(member, module_type)
            and not member is module_type
        ):
            return member(**kwargs)
