# syntax=docker/dockerfile:1

# Setting up Python.
FROM sentiment_pipeline_base:latest
WORKDIR /app
ENV PYTHONPATH "/app/base:/app/streaming_api"

# Installs python dependencies etc.
COPY requirements.txt requirements.txt
RUN pip install --upgrade pip && \
    pip install -r requirements.txt
COPY . /app/

CMD ["python3", "-m", "streaming_api"]
