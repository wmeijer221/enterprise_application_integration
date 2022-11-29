# syntax=docker/dockerfile:1

# Setting up Python.
FROM python:3.8-slim-buster
WORKDIR /src
COPY requirements.txt requirements.txt
RUN pip install --upgrade pip && \
    pip install -r requirements.txt
COPY . .

# Setting up Java.
RUN apt update \
    && apt upgrade \
    && apt -y install openjdk-11-jre

CMD ["python", "./src/main.py"]
