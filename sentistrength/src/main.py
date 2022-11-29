from adapter import SentistrengthAdapter
from wrapper import SentistrengthWrapper

with SentistrengthWrapper() as wrapper: 
    adapter = SentistrengthAdapter(wrapper)

