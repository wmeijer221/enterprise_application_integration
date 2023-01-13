import logging
import json
from bson import json_util
from os import getenv
from storage_service.mongo_db import MongoDB
from base.canonical_model.review import Review
from base.canonical_model.review_sentiment import ReviewSentiment
from base.channel_messaging import ChannelMessage, create_connection, receive_from_queue, publish_to_queue, start_consuming
from storage_service._version import VERSION

LOGGER = logging.getLogger(__name__)

MONGO_DB_HOST_KEY = "MONGO_DB_HOST"
MONGO_DB_PORT_KEY = "MONGO_DB_PORT"
MONGO_DB_USERNAME_KEY = "MONGO_DB_USERNAME"
MONGO_DB_PASSWORD_KEY = "MONGO_DB_PASSWORD"
MONGO_DB_DATABASE_KEY = "MONGO_DB_DATABASE"
MONGO_DB_AUTHSOURCE_KEY = "MONGO_DB_AUTHSOURCE"
RABBIT_MQ_HOST_KEY = "RABBIT_MQ_HOST"
NEW_REVIEW_IN_KEY = "NEW_REVIEW_IN"
NEW_SENTIMENT_IN_KEY = "NEW_SENTIMENT_IN"


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

        # RabbitMQ instance
        rabbit_mq_host = getenv(RABBIT_MQ_HOST_KEY)
        new_review_in = getenv(NEW_REVIEW_IN_KEY)
        new_sentiment_in = getenv(NEW_SENTIMENT_IN_KEY)
        create_connection(rabbit_mq_host)
        receive_from_queue(new_review_in, self.__new_review_callback, Review)
        receive_from_queue(new_sentiment_in, self.__new_sentiment_callback, ReviewSentiment)
        start_consuming()

    def __new_review_callback(self, message: ChannelMessage):
        payload_dict = vars(message.body)
        inserted_id = self.mongo.getDB().reviews.insert_one(payload_dict).inserted_id
        LOGGER.debug(f"Inserted document {inserted_id} in MongoDB")

    def __new_sentiment_callback(self, message: ChannelMessage):
        payload_dict = vars(message.body)
        review_uuid = payload_dict.pop("review_uuid")
        sentiment_dict = {"sentiment": payload_dict}
        filter_query = {"uuid": review_uuid}
        update_result = self.mongo.getDB().reviews.update_one(filter_query, {"$set": sentiment_dict})
        LOGGER.debug(f"Added sentiment to {update_result.modified_count} document(s) of {update_result.matched_count} matches in MongoDB")
