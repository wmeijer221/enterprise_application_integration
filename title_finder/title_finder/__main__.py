import logging 
from os import getenv
import time

from base._version import VERSION as BASE_VERSION
from title_finder._version import VERSION
from title_finder.tmdb_finder import TMDBFinder

logging.basicConfig(level=logging.INFO)

logo = f"""
  _____ _ _   _        _____ _           _           
 |_   _(_) |_| | ___  |  ___(_)_ __   __| | ___ _ __ 
   | | | | __| |/ _ \ | |_  | | '_ \ / _` |/ _ \ '__|
   | | | | |_| |  __/ |  _| | | | | | (_| |  __/ |   
   |_| |_|\__|_|\___| |_|   |_|_| |_|\__,_|\___|_|   

                                    (v{VERSION} - b{BASE_VERSION})                                                   
"""
logging.info(logo)

delay = int(getenv("START_DELAY"))
time.sleep(delay)

title_finder = TMDBFinder()
title_finder.start_collecting()
