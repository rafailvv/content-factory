import asyncio
from datetime import datetime

from telethon import TelegramClient

from config import Config
from fetcher import Fetcher


async def do_post(cfg: Config):
    tele_client = TelegramClient(cfg.session_name, cfg.api_id, cfg.api_hash)
    await tele_client.start()
    fetcher = Fetcher(client=tele_client, channels=cfg.source_channels)
    posts = await fetcher.fetch_between(datetime(2025, 7, 25, 10,0,0))
    print("Список постов:", posts)
    await tele_client.disconnect()

async def main():
    cfg = Config()
    print("Бот запустился")

    print("Выполняется поиск...")
    await do_post(cfg)

if __name__ == '__main__':
    asyncio.run(main())