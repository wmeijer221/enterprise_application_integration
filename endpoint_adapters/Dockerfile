# syntax=docker/dockerfile:1

# Setting up Python.
FROM sentiment_pipeline_base:latest
WORKDIR /app

# Installs python dependencies etc.
COPY requirements.txt requirements.txt
RUN pip install --upgrade pip && \
    pip install -r requirements.txt
COPY . /app/

CMD ["python3", "-m", "endpoint_adapters"]
