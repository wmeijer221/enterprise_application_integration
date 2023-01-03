import logging
import json
from bson import json_util
from os import getenv
from storage_service.mongo_db import MongoDB
from storage_service.queue_consumer import QueueConsumer
from storage_service._version import VERSION

LOGGER = logging.getLogger(__name__)

MONGO_DB_HOST_KEY = "MONGO_DB_HOST"
MONGO_DB_PORT_KEY = "MONGO_DB_PORT"
MONGO_DB_USERNAME_KEY = "MONGO_DB_USERNAME"
MONGO_DB_PASSWORD_KEY = "MONGO_DB_PASSWORD"
MONGO_DB_DATABASE_KEY = "MONGO_DB_DATABASE"
MONGO_DB_AUTHSOURCE_KEY = "MONGO_DB_AUTHSOURCE"

class StorageService:

    def __init__(self):
        # MongoDB instance
        mongo_db_host = getenv(MONGO_DB_HOST_KEY)
        mongo_db_port = getenv(MONGO_DB_PORT_KEY)
        mongo_db_username = getenv(MONGO_DB_USERNAME_KEY)
        mongo_db_password = getenv(MONGO_DB_PASSWORD_KEY)
        mongo_db_database = getenv(MONGO_DB_DATABASE_KEY)
        mongo_db_authsource = getenv(MONGO_DB_AUTHSOURCE_KEY)
        self.mongo = MongoDB(mongo_db_host, mongo_db_port, mongo_db_username, mongo_db_password, mongo_db_database, mongo_db_authsource)
        
        # Queue consumer instance
        self.queue_consumer = QueueConsumer()
        # LOGGER.debug("Create consumer for queue new_review")
        # self.queue_names = json.loads(getenv(QUEUE_NAMES_KEY))
        self.queue_consumer.add_queue_consumer('new_review', self.__new_review_callback)
        self.queue_consumer.add_queue_consumer('new_sentiment', self.__new_sentiment_callback)
        self.queue_consumer.start_consuming()

    def __new_review_callback(self, channel, method, properties, body):
        payload = body.decode()
        payload_dict = json_util.loads(payload)['body']
        # LOGGER.debug("Storing new review:\n" + payload)
        inserted_id = self.mongo.getDB().reviews.insert_one(payload_dict).inserted_id
        LOGGER.debug(f"Inserted document {inserted_id} in MongoDB")

    def __new_sentiment_callback(self, channel, method, properties, body):
        payload = body.decode()
        payload_dict = json_util.loads(payload)['body']
        review_uuid = payload_dict.pop("review_uuid")
        sentiment_dict = {"sentiment": payload_dict}
        filter_query = {"uuid": review_uuid}
        # LOGGER.debug("Storing new sentiment:\n" + json.dumps(sentiment_dict))
        update_result = self.mongo.getDB().reviews.update_one(filter_query, {"$set": sentiment_dict})
        LOGGER.debug(f"Updated {update_result.modified_count} document(s) of {update_result.matched_count} matches in MongoDB")
