"""Root file for the streaming api module"""

import asyncio
from base64 import decode
import json
from os import getenv
from urllib.parse import urlparse
import aio_pika
import websockets

from websockets.server import WebSocketServerProtocol

RABBIT_MQ_HOST_KEY = "RABBIT_MQ_HOST"
NEW_SENTIMENT_OUT_KEY = "NEW_SENTIMENT_OUT"


class StreamingApi:
    CLIENTS = dict()

    def __init__(self):
        self.rabbit_mq_host = getenv(RABBIT_MQ_HOST_KEY)
        self.new_sentiment = getenv(NEW_SENTIMENT_OUT_KEY)

        print(f"Listen to channel: {self.new_sentiment}")

    async def start_queue_consumer(self):
        print("Starting queue consumer")
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
            print(f"Sending to {len(self.CLIENTS)} clients")

            message_body = json.loads(message.body.decode())

            title_id = message_body.get("body").get("title_id")

            print(f"Title id: {title_id}")

            for client, client_title_id in self.CLIENTS.items():
                print("client_title_id", client_title_id)
                print("title_id", title_id)
                if client_title_id == title_id:
                    await client.send(message.body.decode())

    async def on_new_connection(self, websocket: WebSocketServerProtocol, path: str):
        print("New connection")

        try:
            # Get "id" path query parameter
            parsed_url = urlparse(path)
            id = parsed_url.query.split("=")[1]

            self.CLIENTS[websocket] = id

            print(self.CLIENTS)

            await websocket.send("Hello")

            while True:
                message = await websocket.recv()
                print(message)

        except websockets.exceptions.ConnectionClosedError:
            print(f"Client {websocket.id} closed connection")
        except Exception as e:
            print(f"Unknown error: {e}")
        finally:
            del self.CLIENTS[websocket]
