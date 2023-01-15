import logging
import json
from bson import json_util
from uuid import uuid4
from os import getenv
from base.mongo_db import MongoDB
from base.canonical_model.title import Title
from base.canonical_model.review import Review
from base.canonical_model.review_sentiment import ReviewSentiment
from base.canonical_model.actor import Actor
from base.channel_messaging import (
    ChannelMessage,
    create_connection,
    receive_from_queue,
    publish_to_queue,
    publish_to_pubsub,
    start_consuming,
)
from storage_service._version import VERSION, NAME
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
NEW_TITLE_OUT_KEY = "NEW_TITLE_OUT"
NEW_ACTOR_OUT_KEY = "NEW_ACTOR_OUT"
NEW_REVIEW_OUT_KEY = "NEW_REVIEW_OUT"
NEW_SENTIMENT_OUT_KEY = "NEW_SENTIMENT_OUT"


class StorageService:
    def __init__(self):
        # MongoDB instance
        mongo_db_host = getenv(MONGO_DB_HOST_KEY)
        mongo_db_port = getenv(MONGO_DB_PORT_KEY)
        mongo_db_username = getenv(MONGO_DB_USERNAME_KEY)
        mongo_db_password = getenv(MONGO_DB_PASSWORD_KEY)
        mongo_db_database = getenv(MONGO_DB_DATABASE_KEY)
        mongo_db_authsource = getenv(MONGO_DB_AUTHSOURCE_KEY)
        self.mongo = MongoDB(
            mongo_db_host,
            mongo_db_port,
            mongo_db_username,
            mongo_db_password,
            mongo_db_database,
            mongo_db_authsource,
        )

        # RabbitMQ instance
        rabbit_mq_host = getenv(RABBIT_MQ_HOST_KEY)
        new_title_in = getenv(NEW_TITLE_IN_KEY)
        new_review_in = getenv(NEW_REVIEW_IN_KEY)
        new_sentiment_in = getenv(NEW_SENTIMENT_IN_KEY)
        new_title_out = getenv(NEW_TITLE_OUT_KEY)
        new_review_out = getenv(NEW_REVIEW_OUT_KEY)
        new_sentiment_out = getenv(NEW_SENTIMENT_OUT_KEY)
        create_connection(rabbit_mq_host)
        self.__new_title_callback = partial(
            StorageService.__basic_match_upsert_from_message,
            self,
            collection="titles",
            match_fields={"uuid": "uuid", "name": "name"},
            data_preprocessor=self.__new_title_preprocessor,
            out_channel=new_title_out,
            out_data_type=Title,
            out_message_type="title",
        )
        self.__new_review_callback = partial(
            StorageService.__basic_match_upsert_from_message,
            self,
            collection="reviews",
            match_fields={
                "uuid": "uuid",
            },
            out_channel=new_review_out,
            out_data_type=Review,
            out_message_type="review",
        )
        self.__new_sentiment_callback = partial(
            StorageService.__basic_match_upsert_from_message,
            self,
            collection="reviews",
            match_fields={
                "uuid": "review_uuid",
            },
            data_preprocessor=self.__new_sentiment_preprocessor,
            out_channel=new_sentiment_out,
            out_data_type=Review,
            out_message_type="review",
        )
        receive_from_queue(new_title_in, self.__new_title_callback, Title)
        receive_from_queue(new_review_in, self.__new_review_callback, Review)
        receive_from_queue(
            new_sentiment_in, self.__new_sentiment_callback, ReviewSentiment
        )
        start_consuming()

    def __basic_match_upsert_from_message(
        self,
        message: ChannelMessage,
        collection: str,
        match_fields: dict = {},
        data_preprocessor: callable = None,
        out_channel: str = None,
        out_data_type: type = None,
        out_message_type: type = None,
    ):
        logging.info(f"Received message: {message.body}")
        # payload_dict = vars(message.body)
        data = message.body
        self.__basic_match_upsert(
            data_obj=data,
            collection=collection,
            match_fields=match_fields,
            data_preprocessor=data_preprocessor,
            out_channel=out_channel,
            out_data_type=out_data_type,
            out_message_type=out_message_type,
        )

    def __basic_match_upsert(
        self,
        data_obj: object,
        collection: str,
        match_fields: dict = {},
        data_preprocessor: callable = None,
        out_channel: str = None,
        out_data_type: type = None,
        out_message_type: type = None,
    ):
        filter_query = {}
        data = vars(data_obj)
        # logging.info(f'vars(data) = {data}')
        if match_fields:
            for collection_match_field, message_match_field in match_fields.items():
                message_match_value = data[message_match_field]
            filter_query[collection_match_field] = message_match_value
        if data_preprocessor:
            data = data_preprocessor(data)
        update_result = self.mongo.getDB()[collection].find_one_and_update(
            filter_query, {"$set": data}, upsert=True, new=True
        )

        if update_result:
            logging.info(f"Upserted document in collection {collection} in MongoDB")

        if out_channel:
            if out_channel == "new_sentiment":
                # For review sentiment, we want to merge it with the review
                del update_result["_id"]
                data = update_result

            out_message = ChannelMessage.channel_message_from(
                message_type=out_message_type,
                sender_type=NAME,
                sender_version=VERSION,
                body=data,
            )

            publish_to_pubsub(out_message, out_channel)

    def __new_title_preprocessor(self, raw_data):
        # Splits and stores cast names in actors collection
        new_actor_out = getenv(NEW_ACTOR_OUT_KEY)
        data = raw_data
        collection = "actors"
        match_fields = {
            "uuid": "uuid",
            "name": "name",
        }
        cast_uuid = []
        for actor in data["cast"]:
            actor_obj = Actor(
                uuid=str(uuid4()),
                name=actor,
            )
            self.__basic_match_upsert(
                data_obj=actor_obj,
                collection=collection,
                match_fields=match_fields,
                out_channel=new_actor_out,
                out_data_type=Actor,
                out_message_type="actor",
            )
            cast_uuid.append(actor_obj.uuid)
        data["cast"] = tuple(cast_uuid)
        return data

    def __new_sentiment_preprocessor(self, raw_data):
        data = {
            "sentiment": {
                "negativity": raw_data["negativity"],
                "polarity": raw_data["polarity"],
                "positivity": raw_data["positivity"],
            }
        }
        return data
