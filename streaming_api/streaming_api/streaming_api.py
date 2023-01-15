"""Root file for the streaming api module"""

import asyncio
from base64 import decode
import json
import logging
from os import getenv
from urllib.parse import urlparse
import aio_pika
import websockets

from websockets.server import WebSocketServerProtocol

RABBIT_MQ_HOST_KEY = "RABBIT_MQ_HOST"
NEW_SENTIMENT_OUT_KEY = "NEW_SENTIMENT_OUT"


class StreamingApi:
    TITLE_CLIENTS = dict()
    ACTOR_CLIENTS = dict()
    actor_ids_for_title = dict()

    def __init__(self):
        self.rabbit_mq_host = getenv(RABBIT_MQ_HOST_KEY)
        self.new_sentiment = getenv(NEW_SENTIMENT_OUT_KEY)

    async def start_queue_consumer(self):
        logging.info("Starting queue consumer")
        # For the Streaming API, we do not use the base image because we need the asynchronous version of pika
        connection = await aio_pika.connect_robust(
            host=self.rabbit_mq_host, login="guest", password="guest"
        )

        channel = await connection.channel()

        # subscribe to new_sentiment pubsub
        new_sentiment_exchange = await channel.declare_exchange(
            self.new_sentiment, aio_pika.ExchangeType.FANOUT
        )

        queue = await channel.declare_queue(exclusive=True)

        await queue.bind(new_sentiment_exchange)

        await queue.consume(self.on_message_received)

    async def on_message_received(self, message: aio_pika.IncomingMessage):
        async with message.process():
            message_body = json.loads(message.body.decode())

            title_id = message_body.get("body").get("title_id")

            if title_id:
                for client, client_title_id in self.TITLE_CLIENTS.items():
                    if client_title_id == title_id:
                        await client.send(
                            json.dumps(
                                {"type": "review", "body": message_body.get("body")}
                            )
                        )

    async def on_new_connection(self, websocket: WebSocketServerProtocol, path: str):
        logging.info(f"New connection: {websocket.id}")
        try:
            # Parse
            entity = path.split("?")[1].split("=")[0]
            parsed_url = urlparse(path)
            id = parsed_url.query.split("=")[1]

            if entity == "title_id":
                self.TITLE_CLIENTS[websocket] = id
            elif entity == "actor_id":
                self.ACTOR_CLIENTS[websocket] = id

            await websocket.send(json.dumps({"type": "connected"}))

            while True:
                await websocket.recv()

        except websockets.exceptions.ConnectionClosedError:
            logging.info(f"Client {websocket.id} closed connection")
        except Exception as e:
            logging.warning(f"Client {websocket.id} left: {e}")
        finally:
            if websocket in self.TITLE_CLIENTS:
                del self.TITLE_CLIENTS[websocket]
            if websocket in self.ACTOR_CLIENTS:
                del self.ACTOR_CLIENTS[websocket]
