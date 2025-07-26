from datetime import datetime, timezone
from typing import List

from telethon import TelegramClient


class Fetcher:
    def __init__(self, client: TelegramClient, channels : List[str]):
        self.channels = channels
        self.client = client

    async def fetch_between(self, last_time : datetime):
        if last_time.tzinfo is None:
            last_time = last_time.replace(tzinfo=timezone.utc)

        posts = []
        for ch in self.channels:
            entity = await self.client.get_entity(ch)
            async for msg in self.client.iter_messages(entity, reverse=False):
                if msg.date >= last_time:
                    posts.append({
                        "id" : msg.id,
                        "channel" : ch,
                        "date" : msg.date,
                        "text" : msg.message or "",
                        "views" : getattr(msg, "views", 0),
                        "forwards" : getattr(msg, "forwards", 0),
                        "reactions": sum(r.count for r in msg.reactions.results) if msg.reactions else 0
                    })
                else:
                    break
        return posts