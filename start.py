import asyncio
import threading
from telethon import TelegramClient

API_ID = "YOUR_API_ID"
API_HASH = "YOUR_API_HASH"
CHANNEL_USERNAME = "YOUR_CHANNEL_USERNAME"
WORKERS = 50
DEL_LIMIT = 100

async def fetch_messages(client, queue):
    async for message in client.iter_messages(CHANNEL_USERNAME):
        await queue.put(message.id)

async def delete_worker(client, queue):
    while True:
        messages = []
        for _ in range(DEL_LIMIT):
            try:
                messages.append(queue.get_nowait())
            except asyncio.QueueEmpty:
                break
        if messages:
            await asyncio.gather(client.delete_messages(CHANNEL_USERNAME, messages))
            print(f"Deleted {len(messages)} messages")

async def main():
    queue = asyncio.Queue()
    async with TelegramClient("usir_died_real", API_ID, API_HASH) as client:
        fetch_task = asyncio.create_task(fetch_messages(client, queue))
        workers = [asyncio.create_task(delete_worker(client, queue)) for _ in range(WORKERS)]
        await fetch_task
        await queue.join()
        for worker in workers:
            worker.cancel()

asyncio.run(main())
