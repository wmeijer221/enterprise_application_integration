# Base Package

This sub-project contains the code that's shared between projects.
Specifically, implementations for the fundamentals of the _message-oriented-architecture_; i.e. communicating with message channels.
Additionally, it implements contains the _canonical data model_ for the project; i.e. objects of which it must be ensured that they have the same format across packages.

To implement the ``base`` package into other sub-projects, make sure its respective ``Dockerfile`` inherits and respects the base image, like:
```Dockerfile
# Setting up base image.
FROM sentiment_pipeline_base:latest
WORKDIR /app
```
Then, to make the package accessible in Python, add the following to the ``__main__.py`` file (in case the project's entrypoint is different, this can, of course, be added elsewhere):
```python
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
```

Consequently, because a dependency on ``base`` is created, the ``base`` package MUST be built prior to building the inheriting docker image, which can be done as follows:
```bash
docker build base --tag sentiment_pipeline_base
```
Additionally, whenever the ``base`` package is updated (e.g. a model is added or a bug is fixed), all inheriting packages must be rebuilt to inherit the made changes.
