from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from asyncpg import Pool

from dld_quiz_bot.db.repository import get_stats

router = Router()


@router.message(Command("stats"))
async def stats_handler(message: Message, pool: Pool) -> None:
    if message.from_user is None:
        return

    stats = await get_stats(pool, message.from_user.id)

    if len(stats) == 0:
        stats_message = "Sie haben noch keine Tests gemacht. Starte jetzt mit /exam! 🎯"
    else:
        total = len(stats)
        avg = sum(s.correct_answers for s in stats) / total
        best = max(s.correct_answers for s in stats)
        last = stats[0]

        stats_message = (
            f"📊 <b>Ihre Statistik</b>\n\n"
            f"Tests abgeschlossen: <b>{total}</b>\n"
            f"Durchschnitt: <b>{avg:.1f}/33</b> ({avg / 33 * 100:.0f}%)\n"
            f"Bestes Ergebnis: <b>{best}/33</b> ({best / 33 * 100:.0f}%)\n\n"
            f"🕐 Letztes Test: <b>{last.correct_answers}/33</b>"
        )

    await message.answer(stats_message)
