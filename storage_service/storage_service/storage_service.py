import logging
import json
from bson import json_util
from os import getenv
from base.mongo_db import MongoDB
from base.canonical_model.title import Title
from base.canonical_model.review import Review
from base.canonical_model.review_sentiment import ReviewSentiment
from base.channel_messaging import ChannelMessage, create_connection, receive_from_queue, publish_to_queue, start_consuming
from storage_service._version import VERSION
from functools import partial, partialmethod


MONGO_DB_HOST_KEY = "MONGO_DB_HOST"
MONGO_DB_PORT_KEY = "MONGO_DB_PORT"
MONGO_DB_USERNAME_KEY = "MONGO_DB_USERNAME"
MONGO_DB_PASSWORD_KEY = "MONGO_DB_PASSWORD"
MONGO_DB_DATABASE_KEY = "MONGO_DB_DATABASE"
MONGO_DB_AUTHSOURCE_KEY = "MONGO_DB_AUTHSOURCE"
RABBIT_MQ_HOST_KEY = "RABBIT_MQ_HOST"
NEW_TITLE_IN_KEY = "NEW_TITLE_IN"
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
        new_title_in = getenv(NEW_REVIEW_IN_KEY)
        new_review_in = getenv(NEW_REVIEW_IN_KEY)
        new_sentiment_in = getenv(NEW_SENTIMENT_IN_KEY)
        create_connection(rabbit_mq_host)
        self.__new_title_callback = partial(
            StorageService.__basic_match_upsert_,
            self,
            collection='titles',
            match_fields={
                "uuid": "uuid",
                "name": "name"
            })
        self.__new_review_callback = partial(
            StorageService.__basic_match_upsert_,
            self,
            collection='reviews',
            match_fields={
                "uuid": "uuid",
            })
        self.__new_sentiment_callback = partial(
            StorageService.__basic_match_upsert_,
            self,
            collection='reviews',
            match_fields={
                "uuid": "review_uuid",
            },
            data_preprocessor=self.__new_sentiment_preprocessor
            )
        receive_from_queue('new_title', self.__new_title_callback, Title)
        receive_from_queue('new_review', self.__new_review_callback, Review)
        receive_from_queue('new_sentiment', self.__new_sentiment_callback, ReviewSentiment)
        start_consuming()

    def __basic_match_upsert_(self, message: ChannelMessage, collection: str, match_fields: dict = {}, data_preprocessor: callable = None):
        logging.info(f'Received message: {message.body}')
        payload_dict = vars(message.body)
        filter_query = {}
        if match_fields:
            for collection_match_field, message_match_field in match_fields.items():
                message_match_value = payload_dict[message_match_field]
            filter_query[collection_match_field] = message_match_value
        if data_preprocessor:
            payload_dict = data_preprocessor(payload_dict)
        update_result = self.mongo.getDB()[collection].update_one(filter_query, {"$set": payload_dict}, upsert=True)
        if update_result.upserted_id:
            logging.info(f'Upserted document {update_result.upserted_id} in collection {collection} in MongoDB')
        else:
            logging.info(f'Updated {update_result.modified_count} document(s) of {update_result.matched_count} matches in collection {collection} MongoDB')

    def __new_sentiment_preprocessor(self, raw_data):
        data = {"sentiment": {"negativity": raw_data['negativity'], "polarity": raw_data['polarity'], "positivity": raw_data['positivity']}}
        return data

