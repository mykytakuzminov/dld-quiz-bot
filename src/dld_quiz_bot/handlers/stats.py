from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from asyncpg import Pool

from dld_quiz_bot.db.models import User
from dld_quiz_bot.db.repository import EXAM_TOTAL, get_stats
from dld_quiz_bot.handlers.middleware import UserMiddleware

router = Router()
router.message.middleware(UserMiddleware())


@router.message(Command("stats"))
async def stats_handler(message: Message, pool: Pool, user: User) -> None:
    if len(stats := await get_stats(pool, user.telegram_id)) == 0:
        stats_message = "Sie haben noch keine Tests gemacht. Starte jetzt mit /exam! 🎯"
    else:
        total = len(stats)
        avg = sum(s.correct_answers for s in stats) / total
        best = max(s.correct_answers for s in stats)
        last = stats[0]

        stats_message = (
            f"📊 <b>Ihre Statistik</b>\n\n"
            f"Tests abgeschlossen: <b>{total}</b>\n"
            f"Durchschnitt: <b>{avg:.0f}/{EXAM_TOTAL}</b> ({avg / EXAM_TOTAL * 100:.0f}%)\n"
            f"Bestes Ergebnis: <b>{best}/{EXAM_TOTAL}</b> ({best / EXAM_TOTAL * 100:.0f}%)\n\n"
            f"🕐 Letztes Test: <b>{last.correct_answers}/{EXAM_TOTAL}</b>"
        )

    await message.answer(stats_message)
