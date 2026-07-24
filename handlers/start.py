from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from keyboards.reply import get_main_menu
from utils.db.queries import get_user
from utils.i18n import _
from utils.loggers import logger
from handlers.register import Register

router = Router()

@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext, lang: str = "uz"):
    user = await get_user(message.from_user.id)
    
    if user:
        welcome_msg = _("welcome", lang=lang, name=user.full_name)
        select_section = {
            "uz": "Menyudan kerakli bo'limni tanlang:",
            "ru": "Выберите нужный раздел из меню:",
            "en": "Select the desired section from the menu:"
        }
        await message.answer(
            f"{welcome_msg}\n{select_section.get(lang, select_section['uz'])}",
            reply_markup=get_main_menu(lang)
        )
        logger.info(f"Qaytgan user | id={message.from_user.id}")
        
    else:
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(text="O'zbekcha 🇺🇿", callback_data="start_lang_uz"),
                    InlineKeyboardButton(text="Русский 🇷🇺", callback_data="start_lang_ru"),
                    InlineKeyboardButton(text="English 🇬🇧", callback_data="start_lang_en")
                ]
            ]
        )
        
        await message.answer(
            f"Salom, {message.from_user.full_name}! 👋\n\n"
            f"Online Lessons botiga xush kelibsiz!\n"
            f"Davom etish uchun muloqot tilini tanlang 👇\n\n"
            f"Пожалуйста, выберите язык для продолжения 👇\n\n"
            f"Please select your language to continue 👇",
            reply_markup=keyboard
        )
        logger.info(f"Yangi user keldi, til tanlash kutilmoqda | id={message.from_user.id}")


@router.callback_query(F.data.startswith("start_lang_"))
async def choose_start_language(callback: CallbackQuery, state: FSMContext):
    selected_lang = callback.data.split("_")[-1]
    
    await state.update_data(lang=selected_lang)
    
    name_prompt = _("register_name", lang=selected_lang)
    
    await callback.message.answer(
        name_prompt,
        reply_markup=None
    )
    await callback.answer()
    await state.set_state(Register.name)
    logger.info(f"Til tanlandi: {selected_lang}. FSM registration boshlandi | id={callback.from_user.id}")