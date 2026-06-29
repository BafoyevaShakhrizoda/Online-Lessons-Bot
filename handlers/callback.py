from aiogram import Router, F
from aiogram.types import CallbackQuery # bu call back query userga ko'rinmasdan ketgan ma'lumotlardan qilingan so'rov

router = Router()

@router.callback_query(F.data == "course_python")  # bu joyida o'sha yashirin kelgan data qabul qilib oladi 
async def course_python(callback: CallbackQuery):
    await callback.message.answer("🐍 Python kursi: 12 darslik, asoslardan OOP gacha.") # keyin unga javob qaytarib yuboradi
    await callback.answer()  # yuklanish belgisini to'xtatish uchun shart

@router.callback_query(F.data == "course_sql")
async def course_sql(callback: CallbackQuery):
    await callback.message.answer("🗄 PostgreSQL kursi: SQL asoslari + Python bilan ulash.")
    await callback.answer()

@router.callback_query(F.data == "course_bot")
async def course_bot(callback: CallbackQuery):
    await callback.message.answer("🤖 Telegram Bot kursi: aiogram bilan to'liq bot yaratish.")
    await callback.answer()