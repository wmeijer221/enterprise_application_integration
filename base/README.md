# Base Package

This sub-project contains the code that's shared between projects.
Specifically, implementations for the fundamentals of the _message-oriented-architecture_; i.e. communicating with message channels.
Additionally, it implements contains the _canonical data model_ for the project; i.e. objects of which it must be ensured that they have the same format across packages.

To implement the ``base`` package into other sub-projects, make sure its respective ``Dockerfile`` inherits and respects the base image, like:
```Dockerfile
# Setting up base image.
FROM sentiment_pipeline_base:latest
WORKDIR /app
ENV PYTHONPATH "/app/base:<PATH_TO_YOUR_PROJECT>"
```

Consequently, because a dependency on ``base`` is created, the ``base`` package MUST be built prior to building the inheriting docker image, which can be done as follows:
```bash
docker build base --tag sentiment_pipeline_base
```
Additionally, whenever the ``base`` package is updated (e.g. a model is added or a bug is fixed), all inheriting packages must be rebuilt to inherit the made changes.
