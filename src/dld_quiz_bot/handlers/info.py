from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

router = Router()


async def send_info(message: Message) -> None:
    info_message = (
        "💁 <b>Verfügbare Befehle</b>\n\n"
        "/start — Bot starten oder neu starten\n"
        "/learn — Einzelne Fragen üben\n"
        "/exam — Vollständigen Test starten\n"
        "/stats — Ihre Testergebnisse anzeigen\n"
        "/settings — Bundesland ändern\n"
        "/stop — Aktuelle Übung beenden\n"
        "/info — Diese Hilfe anzeigen"
    )

    await message.answer(info_message)


@router.message(Command("info"))
async def info_handler(message: Message) -> None:
    await send_info(message)
