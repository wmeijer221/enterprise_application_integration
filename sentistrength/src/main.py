from adapter import SentistrengthAdapter
from wrapper import SentistrengthWrapper

with SentistrengthWrapper() as wrapper: 
    adapter = SentistrengthAdapter(wrapper)
    print(wrapper.get_sentiment("Some\nillegal\rstring"))

