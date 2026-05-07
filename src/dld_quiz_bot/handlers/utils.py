from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State
from aiogram.types import FSInputFile, KeyboardButton, Message, ReplyKeyboardMarkup

from dld_quiz_bot.db.models import Question
from dld_quiz_bot.enums import AnswerResult
from dld_quiz_bot.paths import find_project_root

BASE_DIR = find_project_root()
IMAGES_DIR = BASE_DIR / "data" / "images"


async def send_question(
    message: Message, question: Question, state: FSMContext, next_state: State
) -> None:
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

    image_path = IMAGES_DIR / f"{question.id}.png"

    await state.set_state(next_state)
    await state.update_data(question=question)
    await message.answer(question_message, reply_markup=keyboard)

    if image_path.exists():
        photo = FSInputFile(image_path)
        await message.answer_photo(photo)


async def check_answer(message: Message, question: Question) -> AnswerResult:
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
            return AnswerResult.INVALID

    if selected == question.correct_answer:
        await message.answer("✅ Richtig!")
        return AnswerResult.CORRECT
    else:
        await message.answer(
            f"❌ <b>Falsch!</b>\n\n<b><i>Richtige Antwort:</i> {question.correct_answer}</b>"
        )
        return AnswerResult.INCORRECT
