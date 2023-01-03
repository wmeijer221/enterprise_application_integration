import json
from fastapi import FastAPI, Depends, WebSocket, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from mongo_db import MongoDB
from bson import json_util
from dotenv import load_dotenv
from os import getenv

import logging

LOGGER = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


MONGO_DB_HOST_KEY = "MONGO_DB_HOST"
MONGO_DB_PORT_KEY = "MONGO_DB_PORT"
MONGO_DB_USERNAME_KEY = "MONGO_DB_USERNAME"
MONGO_DB_PASSWORD_KEY = "MONGO_DB_PASSWORD"
MONGO_DB_DATABASE_KEY = "MONGO_DB_DATABASE"
MONGO_DB_AUTHSOURCE_KEY = "MONGO_DB_AUTHSOURCE"

load_dotenv()
mongo_db_host = getenv(MONGO_DB_HOST_KEY)
mongo_db_port = getenv(MONGO_DB_PORT_KEY)
mongo_db_username = getenv(MONGO_DB_USERNAME_KEY)
mongo_db_password = getenv(MONGO_DB_PASSWORD_KEY)
mongo_db_database = getenv(MONGO_DB_DATABASE_KEY)
mongo_db_authsource = getenv(MONGO_DB_AUTHSOURCE_KEY)

mongo = MongoDB(mongo_db_host, mongo_db_port, mongo_db_username, mongo_db_password, mongo_db_database, mongo_db_authsource)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Define API endpoints

@app.get("/")
async def root():
    """
    Get the online status of the web API
    """
    return {"online": True}

@app.get("/reviews")
async def getAllReviews():
    """
    Get all reviews from storage
    """
    data = [review for review in mongo.getDB().reviews.find({})]
    return json.loads(json_util.dumps(data))

@app.get("/reviews/{title}")
async def getReviewsByTitle(title):
    """
    Get all reviews from storage
    """
    data = [review for review in mongo.getDB().reviews.find({"title": title})]
    return json.loads(json_util.dumps(data))