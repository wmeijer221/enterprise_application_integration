from sentistrength_adapter.adapter import SentistrengthAdapter
from sentistrength_adapter.wrapper import SentistrengthWrapper

import logging 

logging.basicConfig(level=logging.WARNING)

with SentistrengthWrapper() as wrapper: 
    adapter = SentistrengthAdapter(wrapper)

