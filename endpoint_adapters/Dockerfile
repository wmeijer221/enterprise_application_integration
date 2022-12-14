# syntax=docker/dockerfile:1

# Setting up Python.
FROM python:3.8-slim-buster
WORKDIR /src

# Setting up Java.
RUN apt update \
    && apt upgrade \
    && apt -y install openjdk-11-jre

# Installs python dependencies etc.
COPY requirements.txt requirements.txt
RUN pip install --upgrade pip && \
    pip install -r requirements.txt
COPY . .

CMD ["python", "-m" "."]
