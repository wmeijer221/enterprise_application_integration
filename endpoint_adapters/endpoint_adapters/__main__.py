"""Root file for the endpoint adapter module"""

from dotenv import load_dotenv
import logging

from base._version import VERSION as BASE_VERSION
from endpoint_adapters._version import VERSION
from endpoint_adapters.endpoint_adapter import EndpointAdapter

logging.basicConfig(level=logging.WARNING)

title = f"""
  _____           _             _       _        _       _             _            
 | ____|_ __   __| |_ __   ___ (_)_ __ | |_     / \   __| | __ _ _ __ | |_ ___ _ __ 
 |  _| | '_ \ / _` | '_ \ / _ \| | '_ \| __|   / _ \ / _` |/ _` | '_ \| __/ _ \ '__|
 | |___| | | | (_| | |_) | (_) | | | | | |_   / ___ \ (_| | (_| | |_) | ||  __/ |   
 |_____|_| |_|\__,_| .__/ \___/|_|_| |_|\__| /_/   \_\__,_|\__,_| .__/ \__\___|_|   
                   |_|                                          |_|                 

                                                                (v{VERSION} - b{BASE_VERSION})
"""
logging.info(title)

load_dotenv()
EndpointAdapter()
