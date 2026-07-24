from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from filters.registered_filter import IsRegistered
from utils.db.queries import (
    get_courses_paginated, count_all_courses,
    get_course, get_lessons_by_course,
    get_lesson, get_lesson_media,
    get_user, enroll_user
)
from utils.i18n import _    # YANGI QO'SHILGAN
from utils.loggers import logger

router = Router()
router.message.filter(IsRegistered())
# YANGI QO'SHILGAN NARSALAR
PAGE_SIZE = 3


#  Pagination keyboard 
def courses_keyboard(
    courses, page: int, total: int
) -> InlineKeyboardMarkup:

    buttons = [
        [InlineKeyboardButton(
            text=f"📘 {c.title}",
            callback_data=f"course_{c.id}"
        )]
        for c in courses
    ]

    nav = []
    total_pages = max(1, (total + PAGE_SIZE - 1) // PAGE_SIZE)

    if page > 0:
        nav.append(InlineKeyboardButton(
            text="⬅️",
            callback_data=f"courses_page_{page - 1}"
        ))

    nav.append(InlineKeyboardButton(
        text=f"{page + 1}/{total_pages}",
        callback_data="courses_page_info"
    ))

    if (page + 1) * PAGE_SIZE < total:
        nav.append(InlineKeyboardButton(
            text="➡️",
            callback_data=f"courses_page_{page + 1}"
        ))

    if nav:
        buttons.append(nav)

    return InlineKeyboardMarkup(inline_keyboard=buttons)


# Kurslar ro'yxati 
@router.message(F.text.in_({"📚 Kurslar", "📚 Курсы", "📚 Courses", "📚️️️️️️ Darsliklar"}))
async def show_courses(message: Message, lang: str = "uz"):
    await _show_page(message, page=0, lang=lang)


async def _show_page(event, page: int, lang: str = "uz"):
    courses = await get_courses_paginated(page=page, size=PAGE_SIZE)
    total   = await count_all_courses()

    if not courses:
        text = _("no_courses", lang=lang)
        if isinstance(event, Message):
            await event.answer(text)
        else:
            await event.message.edit_text(text)
        return

    keyboard = courses_keyboard(courses, page, total)
    text     = _("courses", lang=lang)

    if isinstance(event, Message):
        await event.answer(text, reply_markup=keyboard)
    else:
        await event.message.edit_text(text, reply_markup=keyboard)


#  Sahifa o'zgarganda 
@router.callback_query(F.data.startswith("courses_page_"))
async def change_page(callback: CallbackQuery, lang: str = "uz"):
    part = callback.data.split("_")[-1]
    if part == "info":
        await callback.answer()
        return

    await _show_page(callback, page=int(part), lang=lang)
    await callback.answer()


@router.callback_query(F.data.startswith("course_"))
async def show_course_detail(callback: CallbackQuery, lang: str = "uz"):
    course_id = int(callback.data.split("_")[1])
    course    = await get_course(course_id)

    if not course:
        err_msg = {
            "uz": "Kurs topilmadi.",
            "ru": "Курс не найден.",
            "en": "Course not found."
        }.get(lang, "Kurs topilmadi.")
        await callback.answer(err_msg, show_alert=True)
        return

    lessons = await get_lessons_by_course(course_id)

    buttons = [
        [InlineKeyboardButton(
            text=f"📖 {lesson.order}. {lesson.title}",
            callback_data=f"lesson_{lesson.id}"
        )]
        for lesson in lessons
    ]

    enroll_btn_text = {
        "uz": "✅ Kursga yozilish",
        "ru": "✅ Записаться на курс",
        "en": "✅ Enroll in course"
    }.get(lang, "✅ Kursga yozilish")

    back_btn_text = {
        "uz": "⬅️ Orqaga",
        "ru": "⬅️ Назад",
        "en": "⬅️ Back"
    }.get(lang, "⬅️ Orqaga")

    buttons += [
        [InlineKeyboardButton(
            text=enroll_btn_text,
            callback_data=f"enroll_{course_id}"
        )],
        [InlineKeyboardButton(
            text=back_btn_text,
            callback_data="courses_page_0"
        )]
    ]

    lessons_label = {
        "uz": f"📝 Darslar: {len(lessons)} ta",
        "ru": f"📝 Уроки: {len(lessons)}",
        "en": f"📝 Lessons: {len(lessons)}"
    }.get(lang, f"📝 Darslar: {len(lessons)} ta")

    await callback.message.edit_text(
        f"📘 <b>{course.title}</b>\n\n"
        f"{course.description or ''}\n\n"
        f"{lessons_label}",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons),
        parse_mode="HTML"
    )
    await callback.answer()


@router.callback_query(F.data.startswith("enroll_"))
async def enroll_to_course(callback: CallbackQuery, lang: str = "uz"):
    course_id = int(callback.data.split("_")[1])
    user      = await get_user(callback.from_user.id)

    if not user:
        err_msg = {
            "uz": "Avval ro'yxatdan o'ting!",
            "ru": "Сначала зарегистрируйтесь!",
            "en": "Please register first!"
        }.get(lang, "Avval ro'yxatdan o'ting!")
        await callback.answer(err_msg, show_alert=True)
        return

    enrolled = await enroll_user(user.id, course_id)
    text     = _("enrolled" if enrolled else "already_enrolled", lang=lang)
    await callback.answer(text, show_alert=True)


@router.callback_query(F.data.startswith("lesson_"))
async def show_lesson(callback: CallbackQuery, lang: str = "uz"):
    lesson_id  = int(callback.data.split("_")[1])
    lesson     = await get_lesson(lesson_id)

    if not lesson:
        err_msg = {
            "uz": "Dars topilmadi.",
            "ru": "Урок не найден.",
            "en": "Lesson not found."
        }.get(lang, "Dars topilmadi.")
        await callback.answer(err_msg, show_alert=True)
        return

    # 1 Dars matni
    text = f"📖 <b>{lesson.title}</b>\n\n"
    if lesson.content:
        text += lesson.content
    if lesson.video_url:
        watch_btn_text = {
            "uz": "Videoni ko'rish",
            "ru": "Смотреть видео",
            "en": "Watch video"
        }.get(lang, "Videoni ko'rish")
        text += f"\n\n🎥 <a href='{lesson.video_url}'>{watch_btn_text}</a>"

    await callback.message.answer(text, parse_mode="HTML")

    # 2 Darsga tegishli barcha medialarni yuboramiz
    media_list = await get_lesson_media(lesson_id)

    for media in media_list:
        if media.media_type == "photo":
            await callback.message.answer_photo(
                photo=media.file_id,
                caption=media.caption
            )
        elif media.media_type == "video":
            await callback.message.answer_video(
                video=media.file_id,
                caption=media.caption
            )
        elif media.media_type == "document":
            await callback.message.answer_document(
                document=media.file_id,
                caption=media.caption
            )
        elif media.media_type == "sticker":
            await callback.message.answer_sticker(
                sticker=media.file_id
            )

    if media_list:
        await callback.message.answer(_("lesson_done", lang=lang))

    await callback.answer()
    logger.info(
        f"Dars ochildi | user={callback.from_user.id} | "
        f"lesson={lesson_id} | media={len(media_list)} ta"
    )