from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def get_main_menu(lang: str = "uz") -> ReplyKeyboardMarkup:
    if lang == "ru":
        profile_btn = "👤 Профиль"
        courses_btn = "📚 Курсы"
        help_btn = "ℹ️ Помощь"
    elif lang == "en":
        profile_btn = "👤 Profile"
        courses_btn = "📚 Courses"
        help_btn = "ℹ️ Help"
    else:
        profile_btn = "👤 Profil"
        courses_btn = "📚 Kurslar"
        help_btn = "ℹ️ Yordam"

    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=profile_btn)],
            [KeyboardButton(text=courses_btn), KeyboardButton(text=help_btn)]
        ],
        resize_keyboard=True
    )

def get_contact_menu(lang: str = "uz") -> ReplyKeyboardMarkup:
    if lang == "ru":
        share_phone = "📱 Поделиться номером"
        cancel = "❌ Отмена"
    elif lang == "en":
        share_phone = "📱 Share contact"
        cancel = "❌ Cancel"
    else:
        share_phone = "📱 Raqamni ulashish"
        cancel = "❌ Bekor qilish"

    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=share_phone, request_contact=True)],
            [KeyboardButton(text=cancel)]
        ],
        resize_keyboard=True
    )

