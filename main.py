import asyncio
from datetime import datetime, timezone, timedelta

from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.types import FSInputFile
from telethon import TelegramClient

from config import Config
from fetcher import Fetcher
from image_generator import ImageGenerator
from rephraser import Rephraser
from scheduler import PostScheduler
from selector import Selector

last_time = datetime.now(timezone.utc) - timedelta(days=1)

async def do_post(cfg: Config):
    global last_time
    tele_client = TelegramClient(cfg.session_name, cfg.api_id, cfg.api_hash)
    await tele_client.start()
    now_time = datetime.now(timezone.utc)
    bot = Bot(token=cfg.telegram_bot_token, default=DefaultBotProperties(parse_mode='Markdown'))

    fetcher = Fetcher(client=tele_client, channels=cfg.source_channels)
    selector = Selector(fetcher, 100)
    rephraser = Rephraser()
    image_gen = ImageGenerator()

    posts = await fetcher.fetch_between(last_time)
    top = await selector.channel_top(posts)
    print("Список постов:", top)
    if top:
        rewritten = rephraser.rewrite(top["text"], cfg.text_style)
        print(f"Текст переписан: {rewritten}")

        img_prompt = rephraser.generate_image_prompt(rewritten, cfg.image_style)
        print(f"Промт для генерации изображения: {img_prompt}")

        img_path = image_gen.generate(img_prompt, filename="out.png")
        print(f"Картинка сохранена: {img_path}")

        photo = FSInputFile(img_path)
        await bot.send_photo(
            chat_id=cfg.target_channel,
            photo=photo,
            caption=rewritten,
        )
        print(f"Опубликовано из @{top['channel']} ({top['id']})")

        last_time = now_time
    else:
        print("Постов не найдено")


    await tele_client.disconnect()
    await bot.session.close()

async def main():
    cfg = Config()
    print("Бот запустился")

    scheduler = PostScheduler(do_post, cfg)
    scheduler.start()
    print("Расписание запущено")

    # print("Выполняется поиск...")
    # await do_post(cfg)

    await asyncio.Event().wait()

if __name__ == '__main__':
    asyncio.run(main())