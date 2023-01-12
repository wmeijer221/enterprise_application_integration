# syntax=docker/dockerfile:1

# Setting up base image.
FROM sentiment_pipeline_base:latest
WORKDIR /app
ENV PYTHONPATH "/app/base:/app/storage_service"

# Installs python dependencies etc.
COPY requirements.txt /app/
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

COPY . /app/

CMD ["python", "-m", "storage_service"]