import json
from fastapi import FastAPI, Depends, WebSocket, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from base.mongo_db import MongoDB
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
    Returns the online status of the API
    """
    return {"online": True}

@app.get("/titles")
async def getAllTitles():
    """
    Returns all titles
    """
    data = [title for title in mongo.getDB().titles.find({})]
    return json.loads(json_util.dumps(data))

@app.get("/titles/search/{query}")
async def getTitlesBySearch(query):
    """
    Returns results of title search
    """
    data = [result for result in mongo.getDB().titles.find({"name": query})]
    return json.loads(json_util.dumps(data))

@app.get("/titles/uuid/{title_uuid}")
async def getTitleById(title_uuid):
    """
    Returns a specifc title based on the provided title uuid
    """
    data = [title for title in mongo.getDB().titles.find({"uuid": title_uuid})]
    return json.loads(json_util.dumps(data))

@app.get("/titles/uuid/{title_uuid}/reviews")
async def getReviewsByTitleId(title_uuid):
    """
    Returns all reviews for a specific title based on the provided title uuid
    """
    data = [review for review in mongo.getDB().reviews.find({"title_id": title_uuid})]
    return json.loads(json_util.dumps(data))

@app.get("/titles/uuid/{title_uuid}/reviews/sentiment")
async def getSentimentByTitleId(title_uuid):
    """
    Returns all sentiments for a specific title based on the provided title uuid
    """
    reviews = [review for review in mongo.getDB().reviews.find({"title_id": title_uuid})]
    reviews_json = json.loads(json_util.dumps(reviews))
    data = [{"review_uuid": review['uuid'], "sentiment": review['sentiment']} for review in reviews_json if 'sentiment' in review.keys()]
    return data

@app.get("/reviews/all")
async def getAllReviews():
    """
    Returns all reviews
    """
    data = [review for review in mongo.getDB().reviews.find({})]
    return json.loads(json_util.dumps(data))