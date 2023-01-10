import logging 

from base._version import VERSION as BASE_VERSION
from title_finder._version import VERSION
from title_finder.tmdb_finder import TMDBFinder

logging.basicConfig(level=logging.INFO)

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

title_finder = TMDBFinder()
title_finder.start_collecting()
