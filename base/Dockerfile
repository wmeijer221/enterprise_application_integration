# syntax=docker/dockerfile:1

FROM python:3.11

RUN mkdir /app
WORKDIR /app

COPY requirements.txt /app/
COPY base /app/base

RUN pip install --upgrade pip && \
    pip install -r requirements.txt
