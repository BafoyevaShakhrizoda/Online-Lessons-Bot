from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from handlers.register import Register
from utils.db.queries import get_user, get_user_courses
from utils.i18n import _
from utils.loggers import logger

router = Router()

@router.message(F.text.in_({"👤 Profil", "👤 Профиль", "👤 Profile"}))
async def show_profile(message: Message, state: FSMContext, lang: str = "uz"):
    user = await get_user(message.from_user.id)

    if not user:
        register_name_prompt = _("register_name", lang=lang)
        await message.answer(register_name_prompt)
        await state.set_state(Register.name)
        return

    courses = await get_user_courses(user.id)
    course_text = ""
    if courses:
        for i, course in enumerate(courses, start=1):
            course_text += f"  {i}. {course.title}\n"
    else:
        # Translate or default: "No courses enrolled yet"
        no_enrolled_msg = {
            "uz": "Hali hech qaysi kursga yozilmagan",
            "ru": "Вы еще не записались ни на один курс",
            "en": "Not enrolled in any courses yet"
        }
        course_text = "  " + no_enrolled_msg.get(lang, no_enrolled_msg["uz"])

    profile_title = _("profile", lang=lang)
    
    name_label = "Ism" if lang == "uz" else "Имя" if lang == "ru" else "Name"
    phone_label = "Telefon" if lang == "uz" else "Телефон" if lang == "ru" else "Phone"
    joined_label = "Ro'yxatdan o'tgan" if lang == "uz" else "Зарегистрирован" if lang == "ru" else "Registered"
    my_courses_label = "Mening kurslarim" if lang == "uz" else "Мои kurсы" if lang == "ru" else "My courses"

    joined_date = user.created_at.strftime('%d.%m.%Y') if user.created_at else ""

    await message.answer(
        f"👤 <b>{profile_title}:</b>\n\n"
        f"<b>{name_label}:</b> {user.full_name}\n"
        f"<b>{phone_label}:</b> {user.phone}\n"
        f"<b>{joined_label}:</b> {joined_date}\n\n"
        f"📚 <b>{my_courses_label}:</b>\n{course_text}",
        parse_mode="HTML"
    )
    logger.info(f"Profil ko'rildi | id={message.from_user.id}")