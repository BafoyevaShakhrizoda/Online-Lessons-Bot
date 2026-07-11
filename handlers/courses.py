from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from utils.db.queries import (
    get_all_courses, get_course,
    get_lessons_by_course, get_lesson,
    get_user, enroll_user
)
from utils.loggers import logger

router = Router()


@router.message(F.text == "📚 Kurslar")
async def show_courses(message: Message):
    courses = await get_all_courses(only_active=True)

    if not courses:
        await message.answer("Hozircha kurslar mavjud emas.")
        return

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(
                text=f"📘 {course.title}",
                callback_data=f"course_{course.id}"
            )]
            for course in courses
        ]
    )
    await message.answer("📚 <b>Mavjud kurslar:</b>", 
                         reply_markup=keyboard, 
                         parse_mode="HTML")


@router.callback_query(F.data.startswith("course_"))
async def show_course_detail(callback: CallbackQuery):
    course_id = int(callback.data.split("_")[1])
    course    = await get_course(course_id)

    if not course:
        await callback.answer("Kurs topilmadi.", show_alert=True)
        return

    lessons = await get_lessons_by_course(course_id)

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(
                text=f"📖 {lesson.title}",
                callback_data=f"lesson_{lesson.id}"
            )]
            for lesson in lessons
        ] + [
            [InlineKeyboardButton(
                text=" Kursga yozilish",
                callback_data=f"enroll_{course_id}"
            )]
        ]
    )

    await callback.message.answer(
        f"📘 <b>{course.title}</b>\n\n"
        f"{course.description}\n\n"
        f"📝 Darslar soni: {len(lessons)}",
        reply_markup=keyboard,
        parse_mode="HTML"
    )
    await callback.answer()


@router.callback_query(F.data.startswith("enroll_"))
async def enroll_to_course(callback: CallbackQuery):
    course_id = int(callback.data.split("_")[1])
    user      = await get_user(callback.from_user.id)

    if not user:
        await callback.answer(
            "Avval ro'yxatdan o'ting!", show_alert=True
        )
        return

    enrolled = await enroll_user(user.id, course_id)

    if enrolled:
        await callback.answer(" Kursga muvaffaqiyatli yozildingiz!", 
                              show_alert=True)
        logger.info(f"Kursga yozildi | user={user.id} | kurs={course_id}")
    else:
        await callback.answer("Siz allaqachon bu kursga yozilgansiz.", 
                              show_alert=True)


@router.callback_query(F.data.startswith("lesson_"))
async def show_lesson(callback: CallbackQuery):
    lesson_id = int(callback.data.split("_")[1])
    lesson    = await get_lesson(lesson_id)

    if not lesson:
        await callback.answer("Dars topilmadi.", show_alert=True)
        return

    text = (
        f"📖 <b>{lesson.title}</b>\n\n"
        f"{lesson.content or 'Kontent mavjud emas.'}"
    )
    if lesson.video_url:
        text += f"\n\n🎥 <a href='{lesson.video_url}'>Videoni ko'rish</a>"

    await callback.message.answer(text, 
                                  parse_mode="HTML",
                                  disable_web_page_preview=False)
    await callback.answer()