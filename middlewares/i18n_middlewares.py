from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from utils.db.queries import get_user


class I18nMiddleware(BaseMiddleware):
    SUPPORTED = ["uz", "ru", "en"]

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        user_id = event.from_user.id if event.from_user else None
        lang = None

        if user_id:
            user = await get_user(user_id)
            if user and user.language:
                lang = user.language

        if not lang and event.from_user:
            lang = event.from_user.language_code

        if lang not in self.SUPPORTED:
            lang = "uz"

        data["lang"] = lang
        return await handler(event, data)