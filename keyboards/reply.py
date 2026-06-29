from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='📚️️️️️️ Darsliklar'),
        KeyboardButton(text='ℹ️ Yordam')],
    ],
    resize_keyboard=True
)
 # bu yerda ikkita tugma yaratib unga nom berilgan