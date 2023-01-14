# syntax=docker/dockerfile:1

# Setting up base image.
FROM sentiment_pipeline_base:latest
WORKDIR /app
ENV PYTHONPATH "/app/base:/app/api"

# Installs python dependencies etc.
COPY requirements.txt requirements.txt
RUN pip install --upgrade pip && \
    pip install -r requirements.txt
COPY . /app/

ENTRYPOINT ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
