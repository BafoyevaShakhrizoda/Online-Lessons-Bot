from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="👤 Profil"),],
        [KeyboardButton(text='📚️️️️️️ Darsliklar'),
        KeyboardButton(text='ℹ️ Yordam')],
        
    ],
    resize_keyboard=True
)
 # bu yerda ikkita tugma yaratib unga nom berilgan
 
contact_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📱 Raqamni ulashish", request_contact=True)],
        [KeyboardButton(text="Bekor qilish")],
    ],
    resize_keyboard=True
)

