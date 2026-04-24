from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import KeyboardButton, Message, ReplyKeyboardMarkup, ReplyKeyboardRemove
from asyncpg import Pool

from dld_quiz_bot.constants import GERMAN_STATES
from dld_quiz_bot.db.repository import create_user, get_user


class Registration(StatesGroup):
    waiting_for_land = State()

router = Router()


@router.message(CommandStart())
async def command_start_handler(message: Message, pool: Pool, state: FSMContext) -> None:
    if message.from_user is None or message.text is None:
        return

    user = await get_user(pool, message.from_user.id)

    if user is None:
        about = (
            "<b>Herzlich Willkommen!</b> 👋\n\n"
            "Ich bin dein Lernbegleiter für den Einbürgerungstest <b>Das Leben in Deutschland</b>.\n\n"
            "Mit mir kannst du alle 310 Fragen üben und dich optimal auf deinen Test vorbereiten.\n\n"
            "Bitte wähle dein Bundesland aus, in dem du den Test ablegen möchtest. 👇"
        )

        keyboard = ReplyKeyboardMarkup(
            keyboard=[[KeyboardButton(text=land)] for land in GERMAN_STATES], resize_keyboard=True
        )

        await state.set_state(Registration.waiting_for_land)
        await message.answer(about, reply_markup=keyboard)
    else:
        welcome_back = (
            "<b>Willkommen zurück!</b> 👋\n\n"
            f"Dein Bundesland: <b>{user.selected_land}</b>.\n"
            "Zum Ändern: /settings"
        )

        await message.answer(welcome_back)


@router.message(Registration.waiting_for_land)
async def german_state_handler(message: Message, pool: Pool, state: FSMContext) -> None:
    if message.from_user is None or message.text is None:
        return

    if message.text in GERMAN_STATES:
        land = f"Ihr Bundesland: {message.text} ✅"

        await message.answer(land, reply_markup=ReplyKeyboardRemove())

        await create_user(
            pool=pool,
            telegram_id=message.from_user.id,
            username=message.from_user.username,
            selected_land=message.text,
        )

        await state.clear()
