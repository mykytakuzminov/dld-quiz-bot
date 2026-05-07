from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove

router = Router()


@router.message(Command("stop"))
async def stop_handler(message: Message, state: FSMContext) -> None:
    await state.clear()
    await message.answer(
        "Gut gemacht! Bis zum nächsten Mal! 👋", reply_markup=ReplyKeyboardRemove()
    )
