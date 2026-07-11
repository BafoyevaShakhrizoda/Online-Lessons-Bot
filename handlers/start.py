from aiogram import Router, F # router bu menejer , F bu kerakli textni tanib olish uchun kerak bo'ladi
from aiogram.filters import CommandStart
from aiogram.types import Message
from keyboards.reply import main_menu # bu yerda 2 ta button chaqirilgan 
from keyboards.inline import courses_menu # bunisida aynan darslik buttonda ishlatish uchun inline buttonlar chaqirlgan
from utils.db.queries import get_user
from utils.loggers import logger



router = Router()

@router.message(CommandStart())
async def cmd_start(message:Message):

    user = await get_user(message.from_user.id)
    
    if user:
        await message.answer(
            f"Xush kelibsiz, {user.full_name}! 👋\n"
            f"Menyudan kerakli bo'limni tanlang:",
            reply_markup=main_menu
        )
        logger.info(f"Qaytgan user | id={message.from_user.id}")
        
    else:
        await message.answer(
            f"Salom, {message.from_user.full_name}! 👋\n\n"
            f"Online Lessons botiga xush kelibsiz!\n"
            f"Davom etish uchun ro'yxatdan o'ting 👇",
            reply_markup=main_menu
        )
        logger.info(f"Yangi user | id={message.from_user.id}")



@router.message(F.text == "ℹ️ Yordam")
async def help_button(message: Message):
    await message.answer("Savollaringiz bo'lsa: @Shahrizoda_Bafoyeva") # bunda aynan yordam degan button bosilganda xabar sifatida ketishi va bot qanday javob qaytarishi berilgan 

@router.message(F.text == "📚️️️️️️ Darsliklar")
async def show_courses(message: Message):
    await message.answer("Qaysi kursni ko'rmoqchisiz?", reply_markup=courses_menu ) # inline button chaqirilgan
    
# bunisida darslik degan buton bosilganda xabar sifatida ketsa, hamda javob ham javobni pastidan inline tugmalar ketgan