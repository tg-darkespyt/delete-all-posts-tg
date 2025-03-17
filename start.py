import asyncio
from telethon import TelegramClient

API_ID = "YOUR_API_ID"
API_HASH = "YOUR_API_HASH"
CHANNEL_USERNAME = "YOUR_CHANNEL_USERNAME"

async def delete_all_posts():
    async with TelegramClient("tg-darkespyt", API_ID, API_HASH) as client:
        messages = []
        async for message in client.iter_messages(CHANNEL_USERNAME):
            messages.append(message.id)
            if len(messages) >= 100:
                await client.delete_messages(CHANNEL_USERNAME, messages)
                print(f"Deleted {len(messages)} messages")
                messages = []
        if messages:
            await client.delete_messages(CHANNEL_USERNAME, messages)
            print(f"Deleted {len(messages)} messages")

asyncio.run(delete_all_posts())
