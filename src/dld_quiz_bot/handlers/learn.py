from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message
from asyncpg import Pool

from dld_quiz_bot.db.models import User
from dld_quiz_bot.db.repository import get_random_question
from dld_quiz_bot.enums import AnswerResult
from dld_quiz_bot.handlers.middleware import UserMiddleware
from dld_quiz_bot.handlers.utils import check_answer, send_question


class Learning(StatesGroup):
    waiting_for_answer = State()
    showing_result = State()


router = Router()
router.message.middleware(UserMiddleware())


async def send_next_question(message: Message, pool: Pool, state: FSMContext, user: User) -> None:
    question = await get_random_question(pool, user.selected_land)

    if question is None:
        await message.answer("🤷 Keine Fragen gefunden.")
        return

    await send_question(message, question, state, Learning.waiting_for_answer)


@router.message(Command("learn"))
async def learn_handler(message: Message, pool: Pool, state: FSMContext, user: User) -> None:
    await send_next_question(message, pool, state, user)


@router.message(Learning.waiting_for_answer, ~Command("stop"))
async def answer_handler(message: Message, pool: Pool, state: FSMContext, user: User) -> None:
    if message.text is None:
        return

    data = await state.get_data()
    question = data["question"]

    match await check_answer(message, question):
        case AnswerResult.CORRECT | AnswerResult.INCORRECT:
            await send_next_question(message, pool, state, user)
        case AnswerResult.INVALID:
            await send_question(message, question, state, Learning.waiting_for_answer)
