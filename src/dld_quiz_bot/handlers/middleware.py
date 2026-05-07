from collections.abc import Awaitable, Callable
from typing import Any

from aiogram import BaseMiddleware
from aiogram.types import Message, TelegramObject

from dld_quiz_bot.db.repository import get_user


class UserMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        if not isinstance(event, Message) or event.from_user is None:
            return await handler(event, data)

        pool = data["pool"]
        user = await get_user(pool, event.from_user.id)

        if user is None:
            await event.answer(
                "⚠️ Sie sind noch nicht registriert.\nBitte starten Sie den Bot mit /start"
            )
            return None

        data["user"] = user
        return await handler(event, data)
