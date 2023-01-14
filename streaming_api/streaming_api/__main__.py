"""Root file for the streaming api module"""

import asyncio
import functools
from websockets.server import serve

from streaming_api.streaming_api import StreamingApi


async def start_queue_consumer():
    queue_consumer = StreamingApi()
    await queue_consumer.start_queue_consumer()


async def start_websocket_server():
    async with serve(
        functools.partial(StreamingApi().on_new_connection), "0.0.0.0", 8082
    ):
        print("Streaming API started")
        await asyncio.Future()


async def main():
    await asyncio.gather(start_queue_consumer(), start_websocket_server())


if __name__ == "__main__":
    asyncio.run(main())
