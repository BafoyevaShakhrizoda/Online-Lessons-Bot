from aiogram.filters import BaseFilter
from aiogram.types import Message, CallbackQuery
from config import ADMIN_ID
from utils.loggers import logger


class IsAdmin(BaseFilter):
    async def __call__(self, event:Message | CallbackQuery): # bo'layotgan hodisa ikkalasi uchun ham ishlashi kerak 
        user_id = event.from_user.id # botdan foydalanganayotgan userni idsini olib tekshirgan 
        is_admin = user_id == ADMIN_ID #configda berilgan adminni idsiga teng bo'lsa
        
        
        if not is_admin: # agar bir xil bo'lmasa 
            logger.warner(f"Ruxsatsiz kirishga urinish | id = {user_id}") # shunaqa log yoziladi 
            
        return is_admin # userga adminlik huquqi berilgan
