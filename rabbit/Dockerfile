# syntax=docker/dockerfile:1

# Setting up Python.
FROM python:3.8-slim-buster
WORKDIR /app/rabbit

# Installs python dependencies etc.
COPY requirements.txt requirements.txt
RUN pip install --upgrade pip && \
    pip install -r requirements.txt
COPY . .

# CMD ["python", "./src/main.py"]
