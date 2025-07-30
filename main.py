import asyncio
from datetime import datetime

from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from telethon import TelegramClient

from config import Config
from fetcher import Fetcher
from selector import Selector


async def do_post(cfg: Config):
    tele_client = TelegramClient(cfg.session_name, cfg.api_id, cfg.api_hash)
    await tele_client.start()
    bot = Bot(token=cfg.telegram_bot_token, default=DefaultBotProperties(parse_mode='Markdown'))

    fetcher = Fetcher(client=tele_client, channels=cfg.source_channels)
    selector = Selector(fetcher, 100)

    posts = await fetcher.fetch_between(datetime(2025, 7, 25, 10,0,0))
    posts = await selector.channel_top(posts)
    print("Список постов:", posts)

    await tele_client.disconnect()
    await bot.session.close()

async def main():
    cfg = Config()
    print("Бот запустился")

    print("Выполняется поиск...")
    await do_post(cfg)

if __name__ == '__main__':
    asyncio.run(main())