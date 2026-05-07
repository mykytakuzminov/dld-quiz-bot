import asyncio
import logging
import sys
from os import getenv

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from dotenv import load_dotenv

from dld_quiz_bot.db.database import close_pool, create_pool
from dld_quiz_bot.handlers.exam import router as exam_router
from dld_quiz_bot.handlers.info import router as info_router
from dld_quiz_bot.handlers.learn import router as learn_router
from dld_quiz_bot.handlers.settings import router as settings_router
from dld_quiz_bot.handlers.start import router as start_router
from dld_quiz_bot.handlers.stats import router as stats_router
from dld_quiz_bot.handlers.stop import router as stop_router

load_dotenv()

TOKEN = getenv("BOT_TOKEN")
POOL = getenv("ASYNCPG_URL")

dp = Dispatcher()

dp.include_router(start_router)
dp.include_router(settings_router)
dp.include_router(stop_router)
dp.include_router(learn_router)
dp.include_router(exam_router)
dp.include_router(stats_router)
dp.include_router(info_router)


async def main() -> None:
    if TOKEN is None:
        raise ValueError("BOT_TOKEN is not set")
    if POOL is None:
        raise ValueError("ASYNCPG_URL is not set")

    pool = await create_pool(POOL)
    try:
        bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
        await dp.start_polling(bot, pool=pool)
    finally:
        await close_pool(pool)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
