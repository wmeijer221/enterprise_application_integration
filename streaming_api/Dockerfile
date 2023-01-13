# syntax=docker/dockerfile:1

FROM python:3.11

RUN mkdir /app
WORKDIR /app

COPY . .

RUN pip install --upgrade pip && \
    pip install -r requirements.txt
