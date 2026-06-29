from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

courses_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="🐍 Python", callback_data="course_python")], # bu yerda agar python degan buttonni bossa loyihaga yashirincha ma'lumot ketadi " course_python" degan
        [InlineKeyboardButton(text="🗄 PostgreSQL", callback_data="course_sql")],# bunda sql degan ketadi
        [InlineKeyboardButton(text="🤖 Telegram Bot", callback_data="course_bot")], # bunisida esa bot degan data ketadi
    ] 
)

# bu yerda xabardan chiqadigan tugmalar yaratilgan