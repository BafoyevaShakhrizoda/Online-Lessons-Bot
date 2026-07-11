from aiogram import Router, F
from aiogram.types import Message

from utils.db.queries import get_user, get_user_courses
from utils.loggers import logger

router = Router()

@router.message(F.text == "👤 Profil")
async def show_profile(message: Message):
    user = await get_user(message.from_user.id)

    if not user:
        await message.answer(
            "Siz hali ro'yxatdan o'tmagansiz.\n"
            "Iltimos, avval ro'yxatdan o'ting."
        )
        return

    courses = await get_user_courses(user.id)
    course_text = ""
    if courses:
        for i, course in enumerate(courses, start=1):
            course_text += f"  {i}. {course.title}\n"
    else:
        course_text = "  Hali hech qaysi kursga yozilmagan"

    await message.answer(
        f"👤 <b>Profilingiz:</b>\n\n"
        f"Ism: {user.full_name}\n"
        f"Telefon: {user.phone}\n"
        f"Ro'yxatdan o'tgan: {user.created_at.strftime('%d.%m.%Y')}\n\n"
        f"📚 <b>Mening kurslarim:</b>\n{course_text}",
        parse_mode="HTML"
    )
    logger.info(f"Profil ko'rildi | id={message.from_user.id}")