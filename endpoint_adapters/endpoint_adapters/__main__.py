"""Root file for the endpoint adapter module"""

import logging
from dotenv import load_dotenv

from endpoint_adapters.endpoint_adapter import EndpointAdapter

logging.basicConfig(level=logging.INFO)
load_dotenv()
EndpointAdapter()
