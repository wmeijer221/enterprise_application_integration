"""Root file for the streaming api module"""

import asyncio
import functools
import logging

from websockets.server import serve

from streaming_api.streaming_api import StreamingApi

logging.basicConfig(level=logging.INFO)

queue_consumer = StreamingApi()


async def start_queue_consumer():
    await queue_consumer.start_queue_consumer()


async def start_websocket_server():
    async with serve(
        functools.partial(queue_consumer.on_new_connection), "0.0.0.0", 8082
    ):
        logging.info("Streaming API started")
        await asyncio.Future()


async def main():
    await asyncio.gather(start_queue_consumer(), start_websocket_server())


if __name__ == "__main__":
    asyncio.run(main())
