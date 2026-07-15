from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import Message
from cachetools import TTLCache
from utils.loggers import logger


class ThrottlingMiddleware(BaseMiddleware):
    def __init__(self, rate_limit: float = 1.0):
        self.cache = TTLCache(maxsize=10_000, ttl=rate_limit)     # Har bir user uchun — 1 soniyada 1 ta xabar

    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any]
    ) -> Any:
        user_id = event.from_user.id

        if user_id in self.cache:             # Juda tez xabar yuborayapti — bloklash
            logger.warning(f"Throttling | id={user_id}")
            await event.answer("⏳ Iltimos, biroz kuting...")             # Bu user 1 soniya ichida ikkinchi xabar yuborayapti
            return

        self.cache[user_id] = True        # Cachega qo'shamiz 
        # 1 soniyadan keyin TTLCache o'zi o'chiradi
        return await handler(event, data)