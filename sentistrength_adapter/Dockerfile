# syntax=docker/dockerfile:1

# Setting up base image.
FROM sentiment_pipeline_base:latest
WORKDIR /app

# Setting up Java.
RUN apt update \
    && apt -y upgrade \
    && apt -y install openjdk-11-jre

# Installs python dependencies etc.
COPY requirements.txt /app/
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

COPY . /app/

CMD ["python", "-m", "sentistrength_adapter"]
