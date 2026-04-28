from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, ReplyKeyboardRemove
from asyncpg import Pool

from dld_quiz_bot.db.repository import get_random_question
from dld_quiz_bot.handlers.utils import check_answer, send_question


class Learning(StatesGroup):
    waiting_for_answer = State()
    showing_result = State()


router = Router()


async def send_next_question(message: Message, pool: Pool, state: FSMContext) -> None:
    if message.from_user is None:
        return
    question = await get_random_question(pool, message.from_user.id)
    if question is None:
        await message.answer("Keine Fragen gefunden.")
        return
    await send_question(message, question, state, Learning.waiting_for_answer)


@router.message(Command("learn"))
async def learn_handler(message: Message, pool: Pool, state: FSMContext) -> None:
    await send_next_question(message, pool, state)


@router.message(Learning.waiting_for_answer, ~Command("stop"))
async def answer_handler(message: Message, pool: Pool, state: FSMContext) -> None:
    if message.from_user is None or message.text is None:
        return

    data = await state.get_data()
    question = data["question"]

    await check_answer(message, question)
    await send_next_question(message, pool, state)


@router.message(Command("stop"))
async def stop_handler(message: Message, state: FSMContext) -> None:
    await state.clear()
    await message.answer(
        "Gut gemacht! Bis zum nächsten Mal! 👋", reply_markup=ReplyKeyboardRemove()
    )
