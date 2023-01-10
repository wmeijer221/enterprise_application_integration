"""Root file for the endpoint adapter module"""

import logging
logging.basicConfig(level=logging.INFO)

# Imports the base module
import importlib
try:
    # According to the docker container structure.
    base = importlib.import_module("base", "..base")
except:
    # According to the repository structure in case it's ran locally.
    import sys
    logging.warning("Failed to load base, trying alternative source.")
    spec = importlib.util.spec_from_file_location("base", "../base/base/__init__.py")
    base = importlib.util.module_from_spec(spec)
    sys.modules["base"] = base
    spec.loader.exec_module(base)
from base._version import VERSION as BASE_VERSION

from dotenv import load_dotenv

from endpoint_adapters._version import VERSION
from endpoint_adapters.endpoint_adapter import EndpointAdapter

title = f"""
  ______           _             _       _                 _             _            
 |  ____|         | |           (_)     | |       /\      | |           | |           
 | |__   _ __   __| |_ __   ___  _ _ __ | |_     /  \   __| | __ _ _ __ | |_ ___ _ __ 
 |  __| | '_ \ / _` | '_ \ / _ \| | '_ \| __|   / /\ \ / _` |/ _` | '_ \| __/ _ \ '__|
 | |____| | | | (_| | |_) | (_) | | | | | |_   / ____ \ (_| | (_| | |_) | ||  __/ |   
 |______|_| |_|\__,_| .__/ \___/|_|_| |_|\__| /_/    \_\__,_|\__,_| .__/ \__\___|_|   
                    | |                                           | |                 
                    |_|                                           |_|                 

                                                                (v{VERSION} - b{BASE_VERSION})
"""
logging.info(title)

load_dotenv()
EndpointAdapter()
