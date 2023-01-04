"""Root file for the endpoint adapter module"""

import logging
logging.basicConfig(level=logging.WARNING)

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

from dotenv import load_dotenv

from endpoint_adapters.endpoint_adapter import EndpointAdapter

load_dotenv()
EndpointAdapter()
