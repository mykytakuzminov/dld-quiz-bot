from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import KeyboardButton, Message, ReplyKeyboardMarkup, ReplyKeyboardRemove
from asyncpg import Pool

from dld_quiz_bot.db.repository import get_random_question


class Learning(StatesGroup):
    waiting_for_answer = State()
    showing_result = State()


router = Router()


async def send_question(message: Message, pool: Pool, state: FSMContext) -> None:
    if message.from_user is None:
        return

    question = await get_random_question(pool, message.from_user.id)
    if question is None:
        await message.answer("Keine Fragen gefunden.")
        return

    question_message = (
        f"❓<b>Frage {question.id}</b>\n\n"
        f"<i>{question.text}</i>\n\n"
        f"<b>A</b>. {question.options[0]}\n"
        f"<b>B</b>. {question.options[1]}\n"
        f"<b>C</b>. {question.options[2]}\n"
        f"<b>D</b>. {question.options[3]}"
    )

    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="A"), KeyboardButton(text="C")],
            [KeyboardButton(text="B"), KeyboardButton(text="D")],
        ],
        resize_keyboard=True,
    )

    await state.set_state(Learning.waiting_for_answer)
    await state.update_data(question=question)
    await message.answer(question_message, reply_markup=keyboard)


@router.message(Command("learn"))
async def learn_handler(message: Message, pool: Pool, state: FSMContext) -> None:
    await send_question(message, pool, state)


@router.message(Learning.waiting_for_answer, ~Command("stop"))
async def answer_handler(message: Message, pool: Pool, state: FSMContext) -> None:
    if message.from_user is None or message.text is None:
        return

    data = await state.get_data()
    question = data["question"]

    match message.text:
        case "A":
            selected = question.options[0]
        case "B":
            selected = question.options[1]
        case "C":
            selected = question.options[2]
        case "D":
            selected = question.options[3]
        case _:
            await message.answer("Bitte antworte mit A, B, C oder D. 👆")
            return

    if selected == question.correct_answer:
        await message.answer("✅ Richtig!")
    else:
        wrong_answer = (
            f"❌ <b>Falsch!</b>\n\n<b><i>Richtige Antwort:</i> {question.correct_answer}</b>"
        )

        await message.answer(wrong_answer)

    await send_question(message, pool, state)


@router.message(Command("stop"))
async def stop_handler(message: Message, state: FSMContext) -> None:
    await state.clear()
    await message.answer(
        "Gut gemacht! Bis zum nächsten Mal! 👋", reply_markup=ReplyKeyboardRemove()
    )
