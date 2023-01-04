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
from base._version import VERSION as BASE_VERSION
logging.debug(f'Starting with: {BASE_VERSION=}')

# Sentistrength logic.
from os import getenv
import nltk
nltk.download('punkt')

from sentistrength_adapter._version import VERSION
from sentistrength_adapter.adapter import SentistrengthAdapter
from sentistrength_adapter.wrapper import SentistrengthWrapper

logging.debug(f'Starting sentistrength adapter version {VERSION}.')

CLASSIFICATION_TYPE_KEY = "CLASSIFICATION_TYPE"
classification = getenv(CLASSIFICATION_TYPE_KEY)

with SentistrengthWrapper(classification=classification) as wrapper:
    adapter = SentistrengthAdapter(wrapper)
