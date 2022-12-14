# syntax=docker/dockerfile:1

# Setting up Python.
FROM python:3.8-slim-buster
WORKDIR /app/endpoint_adapters

# Installs python dependencies etc.
COPY requirements.txt requirements.txt
RUN pip install --upgrade pip && \
    pip install -r requirements.txt
COPY . .

# CMD ["python", "-m" "endpoint_adapters"]
