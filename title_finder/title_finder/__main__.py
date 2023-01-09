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

from title_finder._version import VERSION
from title_finder.simple_finder import SimpleTitleFinder

logo = f"""
  _______ _ _   _        ______ _           _           
 |__   __(_) | | |      |  ____(_)         | |          
    | |   _| |_| | ___  | |__   _ _ __   __| | ___ _ __ 
    | |  | | __| |/ _ \ |  __| | | '_ \ / _` |/ _ \ '__|
    | |  | | |_| |  __/ | |    | | | | | (_| |  __/ |   
    |_|  |_|\__|_|\___| |_|    |_|_| |_|\__,_|\___|_|   

                                    (v{VERSION} - b{BASE_VERSION})                                                   
"""
logging.info(logo)

SimpleTitleFinder()
