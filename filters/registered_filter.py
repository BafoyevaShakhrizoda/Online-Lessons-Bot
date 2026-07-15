from aiogram.filters import BaseFilter
from aiogram.types import Message
from utils.db.queries import get_user
from utils.loggers import logger


class IsRegistered(BaseFilter): # bu yerda registrdan user o'tgan o'tmaganligini tekshirish 
    async def __call__(self, event=Message) :
        user = await get_user(event.from_user.id) # bo'layotgan xodisani Messsage sifatida olish  databazadagi user bilan botdagi tekshirilgan 
        
        if not user:
            logger.info(f"Ro'yxatdan o'tmagan user | id = {event.from_user.id}") # agar mos kelamasa log sifatida boradigan xabar yozilgan 
        
        return user is not None # user hech qachon none qaytmasligi kerak 
    
    

