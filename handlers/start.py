from aiogram import Router, F # router bu menejer , F bu kerakli textni tanib olish uchun kerak bo'ladi
from aiogram.filters import CommandStart
from aiogram.types import Message
from keyboards.reply import main_menu # bu yerda 2 ta button chaqirilgan 
from keyboards.inline import courses_menu # bunisida aynan darslik buttonda ishlatish uchun inline buttonlar chaqirlgan



router = Router()

@router.message(CommandStart())
async def cmd_start(message:Message):
    await message.answer(
        f"Assalomu alaykum,{message.from_user.full_name}! 👋️️️️️️\nOnline Lessons botimizga xush kelibsiz!",
        reply_markup = main_menu
    ) # startni bosganimizda birinchi bo'lib userga ko'rinadigan javob

@router.message(F.text == "ℹ️ Yordam")
async def help_button(message: Message):
    await message.answer("Savollaringiz bo'lsa: @Shahrizoda_Bafoyeva") # bunda aynan yordam degan button bosilganda xabar sifatida ketishi va bot qanday javob qaytarishi berilgan 

@router.message(F.text == "📚️️️️️️ Darsliklar")
async def show_courses(message: Message):
    await message.answer("Qaysi kursni ko'rmoqchisiz?", reply_markup=courses_menu ) # inline button chaqirilgan
    
# bunisida darslik degan buton bosilganda xabar sifatida ketsa, hamda javob ham javobni pastidan inline tugmalar ketgan