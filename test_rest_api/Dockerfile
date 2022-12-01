FROM python:3.8-slim as base

WORKDIR /src
COPY requirements.txt requirements.txt
RUN pip install --upgrade pip && \
    pip install -r requirements.txt
COPY . .

CMD ["python", "./src/main.py"]
