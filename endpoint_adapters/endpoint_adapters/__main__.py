"""Root file for the endpoint adapter module"""
# type: ignore

import logging
from dotenv import load_dotenv

from endpoint_adapters.endpoint_adapter_composition import EndpointAdapterComposition

logging.basicConfig(level=logging.INFO)
load_dotenv()
EndpointAdapterComposition()
