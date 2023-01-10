import logging 

# Sentistrength logic.
from os import getenv
import nltk

from base._version import VERSION as BASE_VERSION
from sentistrength_adapter._version import VERSION
from sentistrength_adapter.adapter import SentistrengthAdapter
from sentistrength_adapter.wrapper import SentistrengthWrapper

logging.basicConfig(level=logging.INFO)

title = f"""
  ____             _   _     _                        _   _     
 / ___|  ___ _ __ | |_(_)___| |_ _ __ ___ _ __   __ _| |_| |__  
 \___ \ / _ \ '_ \| __| / __| __| '__/ _ \ '_ \ / _` | __| '_ \ 
  ___) |  __/ | | | |_| \__ \ |_| | |  __/ | | | (_| | |_| | | |
 |____/ \___|_| |_|\__|_|___/\__|_|  \___|_| |_|\__, |\__|_| |_|
                                                |___/           

                                        (v{VERSION} - b{BASE_VERSION})
"""
logging.info(title)

CLASSIFICATION_TYPE_KEY = "CLASSIFICATION_TYPE"
classification = getenv(CLASSIFICATION_TYPE_KEY)

nltk.download('punkt')

with SentistrengthWrapper(classification=classification) as wrapper:
    adapter = SentistrengthAdapter(wrapper)
