from os import getenv
import logging 
import nltk
nltk.download('punkt')

from sentistrength_adapter.adapter import SentistrengthAdapter
from sentistrength_adapter.wrapper import SentistrengthWrapper


logging.basicConfig(level=logging.WARNING)

CLASSIFICATION_TYPE_KEY = "CLASSIFICATION_TYPE"
classification = getenv(CLASSIFICATION_TYPE_KEY)

with SentistrengthWrapper(classification=classification) as wrapper:
    adapter = SentistrengthAdapter(wrapper)
