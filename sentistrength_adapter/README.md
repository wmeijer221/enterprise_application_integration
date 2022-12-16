# Sentistrength Adapter

## General

Implements a wrapper and an adapter for the Sentistrength JAR file.

_Note: the JAR file and the corresponding datafiles are not provided with this adapter as they are subject to licenses / distribution restrictions. For any details on how to acquire the JAR, see [this link](http://sentistrength.wlv.ac.uk/)._

To use this tool, some version of java must be installed.
Java 11 was used during the implementation.

## User Guide

### Wrapper

The easiest way to implement the wrapper is as follows:

```python
from wrapper import SentistrengthWrapper

with SentistrengthWrapper() as wrapper:
    result = wrapper.get_sentiment("This wrapper is the best!")
```

Alternatively, you could do:

```python
from wrapper import SentistrengthWrapper

wrapper = SentistrengthWrapper()
wrapper.connect()
result = wrapper.get_sentiment("This wrapper is the best!")
wrapper.disconnect()
```

By default, the wrapper uses the sentistrength files stored in `./data/` and the JAR file in `./jars/`.
However, the constructor of the wrapper can be used to change both of these.
Additionally, by default the wrapper uses `trinary` classification, which can be changed to `binary` or `scale` in the constructor as well.

### Adapter

The easiest way to implement the adapter is as follows:

```python
from adapter import SentistrengthAdapter
from wrapper import SentistrengthWrapper

with SentistrengthWrapper() as wrapper:
    adapter = SentistrengthAdapter(wrapper)
```
