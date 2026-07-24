from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

admin_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="📊 Statistika",       callback_data="admin_stats")],
        [InlineKeyboardButton(text="📚 Kurslar boshqaruvi", callback_data="admin_courses")],
        [InlineKeyboardButton(text="👥 Foydalanuvchilar", callback_data="admin_users")],
        [InlineKeyboardButton(text="📢 Broadcast",        callback_data="admin_broadcast")],
    ]
)

courses_admin_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="➕ Kurs qo'shish",   callback_data="admin_add_course")],
        [InlineKeyboardButton(text="📋 Kurslar ro'yxati", callback_data="admin_list_courses")],
        [InlineKeyboardButton(text="⬅️ Orqaga",          callback_data="admin_back")],
    ]
)


cancel_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="❌ Bekor qilish", callback_data="admin_cancel")]
    ]
)


def course_actions_kb(course_id: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(
                text="➕ Dars qo'shish",
                callback_data=f"admin_add_lesson_{course_id}"
            )],
            [InlineKeyboardButton(
                text="✏️ Kursni tahrirlash",
                callback_data=f"admin_edit_course_{course_id}"
            )],
            [InlineKeyboardButton(
                text="🗑 Kursni o'chirish",
                callback_data=f"admin_delete_course_{course_id}"
            )],
            [InlineKeyboardButton(
                text="📋 Darslar ro'yxati",
                callback_data=f"admin_lessons_{course_id}"
            )],
            [InlineKeyboardButton(text="⬅️ Orqaga", callback_data="admin_list_courses")],
        ]
    )


def lesson_actions_kb(lesson_id: int, course_id: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(
                text="🖼 Media qo'shish",      #  yangi
                callback_data=f"admin_add_media_{lesson_id}"
            )],
            [InlineKeyboardButton(
                text="📎 Media ro'yxati",       #  yangi
                callback_data=f"admin_media_list_{lesson_id}_{course_id}"
            )],
            [InlineKeyboardButton(
                text="✏️ Tahrirlash",
                callback_data=f"admin_edit_lesson_{lesson_id}"
            )],
            [InlineKeyboardButton(
                text="🗑 O'chirish",
                callback_data=f"admin_delete_lesson_{lesson_id}"
            )],
            [InlineKeyboardButton(
                text="⬅️ Orqaga",
                callback_data=f"admin_lessons_{course_id}"
            )],
        ]
    )