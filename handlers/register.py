from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from keyboards.reply import get_main_menu, get_contact_menu
from utils.db.queries import add_user
from utils.i18n import _
from utils.loggers import logger

router = Router()


class Register(StatesGroup):
    name  = State()
    phone = State()


@router.message(Register.name)
async def get_name(message: Message, state: FSMContext):
    state_data = await state.get_data()
    lang = state_data.get("lang", "uz")
    
    await state.update_data(name=message.text)
    
    phone_prompt = _("register_phone", lang=lang)
    
    await message.answer(
        phone_prompt,
        reply_markup=get_contact_menu(lang)
    )
    await state.set_state(Register.phone)


@router.message(Register.phone, F.contact)
async def get_phone(message: Message, state: FSMContext):
    data  = await state.get_data()
    name  = data["name"]
    lang  = data.get("lang", "uz")
    phone = message.contact.phone_number

    await add_user(
        tg_id=message.from_user.id,
        full_name=name,
        phone=phone,
        language=lang
    )
    logger.info(f"Ro'yxatdan o'tish yakunlandi | id={message.from_user.id} | ism={name} | til={lang}")

    welcome_text = _("welcome", lang=lang, name=message.from_user.first_name)
    reg_done_text = _("register_done", lang=lang)

    await message.answer(
        f"{reg_done_text}\n\n{welcome_text}",
        reply_markup=get_main_menu(lang)
    )
    await state.clear()


@router.message(Register.phone, F.text.in_({"❌ Bekor qilish", "Bekor qilish", "❌ Отмена", "❌ Cancel"}))
async def cancel_register(message: Message, state: FSMContext):
    state_data = await state.get_data()
    lang = state_data.get("lang", "uz")
    
    logger.info(f"Ro'yxatdan o'tish bekor qilindi | id={message.from_user.id}")
    await state.clear()
    await message.answer(_("cancelled", lang=lang), reply_markup=get_main_menu(lang))