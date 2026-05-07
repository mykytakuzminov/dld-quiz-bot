from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import KeyboardButton, Message, ReplyKeyboardMarkup, ReplyKeyboardRemove
from asyncpg import Pool

from dld_quiz_bot.db.repository import (
    EXAM_GENERAL,
    EXAM_LAND,
    EXAM_TOTAL,
    create_exam_record,
    get_general_questions,
    get_land_questions,
)
from dld_quiz_bot.enums import AnswerResult
from dld_quiz_bot.handlers.utils import check_answer, check_user_registered, send_question


class Exam(StatesGroup):
    confirming_test_beginning = State()
    waiting_for_answer = State()


router = Router()


@router.message(Command("exam"))
async def exam_handler(message: Message, state: FSMContext) -> None:
    intro_message = (
        "📋 <b>Das Leben in Deutschland</b>\n\n"
        f"Der Test besteht aus <b>{EXAM_TOTAL} Fragen</b>:\n"
        f"- Die ersten <b>{EXAM_GENERAL} Fragen</b> sind für alle Bundesländer gleich\n"
        f"- Die letzten <b>{EXAM_LAND} Fragen</b> beziehen sich auf Ihr Bundesland\n\n"
        "Bei jeder Frage gibt es <b>4 Antwortmöglichkeiten</b> - nur eine ist richtig.\n\n"
        "Drücken Sie auf <b>'Starten'</b>, um den Test zu beginnen 👇"
    )

    keyboard = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="Starten")]], resize_keyboard=True
    )

    await state.set_state(Exam.confirming_test_beginning)
    await message.answer(intro_message, reply_markup=keyboard)


@router.message(Exam.confirming_test_beginning, F.text == "Starten")
async def start_exam_handler(message: Message, pool: Pool, state: FSMContext) -> None:
    if message.from_user is None:
        return

    if (user := await check_user_registered(message, pool)) is None:
        return

    general_questions = await get_general_questions(pool)
    land_questions = await get_land_questions(pool, user.selected_land)

    if len(questions := general_questions + land_questions) == 0:
        await message.answer(
            "⚠️ Fragen konnten nicht geladen werden.", reply_markup=ReplyKeyboardRemove()
        )
        await state.clear()
        return

    await state.update_data(questions=questions, current_index=0, correct_count=0)
    await send_question(message, questions[0], state, Exam.waiting_for_answer)


@router.message(Exam.waiting_for_answer, ~Command("stop"))
async def exam_answer_handler(message: Message, pool: Pool, state: FSMContext) -> None:
    if message.from_user is None or message.text is None:
        return

    data = await state.get_data()
    questions = data["questions"]
    current_index = data["current_index"]
    correct_count = data["correct_count"]

    match await check_answer(message, questions[current_index]):
        case AnswerResult.CORRECT:
            correct_count += 1
            current_index += 1
        case AnswerResult.INCORRECT:
            current_index += 1

    await state.update_data(current_index=current_index, correct_count=correct_count)

    if current_index >= EXAM_TOTAL:
        await create_exam_record(pool, message.from_user.id, correct_count)
        await message.answer(
            f"🎉 Ergebnis: {correct_count}/{len(questions)}", reply_markup=ReplyKeyboardRemove()
        )
        await state.clear()
        return

    await send_question(message, questions[current_index], state, Exam.waiting_for_answer)
