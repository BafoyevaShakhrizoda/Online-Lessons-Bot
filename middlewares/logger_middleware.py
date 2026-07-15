from typing import Callable,Dict,Any,Awaitable
from aiogram import BaseMiddleware
from aiogram.types import Message
from utils.loggers import logger

class LoggerMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Message, Dict[str,Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any],
    ) :
        user = event.from_user
        logger.info(f"Xabar keldi |"
                    f"id={user.id} |" 
                    f"ism={user.full_name}"
                    f"matn={event.text!r}"
                    )
        result = await handler(event,data)
        
        return result 
    
