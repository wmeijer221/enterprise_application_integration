from endpoint_adapters.adapters.api_adapter import APIAdapter
from endpoint_adapters.utils.import_helper import get_instance_of_type_from

def get_adapter_of_type(type: str, publish: callable) -> APIAdapter:
    """Returns API Adapter of provided type."""
    module_path = f"endpoint_adapters.adapters.{type}_adapter"
    return get_instance_of_type_from(
            module_type=APIAdapter,
            module_path=module_path,
            publish=publish,
        )
