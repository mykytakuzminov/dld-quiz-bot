import asyncio
import logging
import sys
from os import getenv

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import KeyboardButton, Message, ReplyKeyboardMarkup, ReplyKeyboardRemove
from asyncpg import Pool

from dld_quiz_bot.constants import GERMAN_STATES
from dld_quiz_bot.database import close_pool, create_pool
from dld_quiz_bot.repository import create_user

TOKEN = getenv("BOT_TOKEN")

dp = Dispatcher()


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    about = (
        "<b>Herzlich Willkommen!</b> 👋\n\n"
        "Ich bin dein Lernbegleiter für den Einbürgerungstest <b>Das Leben in Deutschland</b>.\n\n"
        "Mit mir kannst du alle 310 Fragen üben und dich optimal auf deinen Test vorbereiten.\n\n"
        "Bitte wähle dein Bundesland aus, in dem du den Test ablegen möchtest. 👇"
    )

    keyboard = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=state)] for state in GERMAN_STATES], resize_keyboard=True
    )

    await message.answer(about, reply_markup=keyboard)


@dp.message()
async def german_state_handler(message: Message, pool: Pool) -> None:
    if message.from_user is None or message.text is None:
        return

    if message.text in GERMAN_STATES:
        state = f"Ihr Bundesland: {message.text} ✅"

        await message.answer(state, reply_markup=ReplyKeyboardRemove())

        await create_user(
            pool=pool,
            telegram_id=message.from_user.id,
            username=message.from_user.username,
            selected_land=message.text,
        )


async def main() -> None:
    if TOKEN is None:
        raise ValueError("BOT_TOKEN is not set")

    pool = await create_pool()
    try:
        bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
        await dp.start_polling(bot, pool=pool)
    finally:
        await close_pool(pool)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
