"""Root file for the endpoint adapter module"""
# type: ignore

import logging
from dotenv import load_dotenv

from endpoint_adapters.api_adapter import APIAdapter

logging.basicConfig(level=logging.INFO)
load_dotenv()
APIAdapter()
