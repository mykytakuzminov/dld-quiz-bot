from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import KeyboardButton, Message, ReplyKeyboardMarkup, ReplyKeyboardRemove
from asyncpg import Pool

from dld_quiz_bot.constants import GERMAN_STATES
from dld_quiz_bot.db.repository import change_user_land


class Settings(StatesGroup):
    confirming = State()
    choosing_land = State()


router = Router()


@router.message(Command("settings"))
async def settings_handler(message: Message, state: FSMContext) -> None:
    confirm_message = "Möchten Sie Ihr Bundesland ändern?"

    keyboard = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="Ja"), KeyboardButton(text="Nein")]], resize_keyboard=True
    )

    await state.set_state(Settings.confirming)
    await message.answer(confirm_message, reply_markup=keyboard)


@router.message(Settings.confirming)
async def confirm_land_change_handler(message: Message, state: FSMContext) -> None:
    if message.text == "Ja":
        land = "Welches Bundesland möchten Sie wählen? 👇"

        keyboard = ReplyKeyboardMarkup(
            keyboard=[[KeyboardButton(text=land)] for land in GERMAN_STATES], resize_keyboard=True
        )

        await state.set_state(Settings.choosing_land)
        await message.answer(land, reply_markup=keyboard)
    else:
        await message.answer("Nichts wird geändert.", reply_markup=ReplyKeyboardRemove())
        await state.clear()


@router.message(Settings.choosing_land)
async def select_new_land_handler(message: Message, pool: Pool, state: FSMContext) -> None:
    if message.from_user is None or message.text is None:
        return

    if message.text in GERMAN_STATES:
        land = f"Ihr neues Bundesland: {message.text} ✅"

        await message.answer(land, reply_markup=ReplyKeyboardRemove())
        await change_user_land(pool, message.from_user.id, message.text)

        await state.clear()
