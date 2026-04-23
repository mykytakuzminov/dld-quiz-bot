import asyncio
import logging
import sys
from os import getenv

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message

from dld_quiz_bot.database import close_pool, create_pool

TOKEN = getenv("BOT_TOKEN")

dp = Dispatcher()


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer("Hello!")


async def main() -> None:
    if TOKEN is None:
        raise ValueError("BOT_TOKEN is not set")

    pool = await create_pool()
    try:
        bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
        await dp.start_polling(bot)
    finally:
        await close_pool(pool)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
