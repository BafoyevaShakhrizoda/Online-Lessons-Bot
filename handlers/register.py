from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from keyboards.reply import main_menu, contact_menu
from utils.db.queries import add_user, get_user
from utils.loggers import logger

router = Router()


class Register(StatesGroup):
    name  = State()
    phone = State()


@router.message(F.text == "👤 Profil")
async def start_register(message: Message, state: FSMContext):
    user = await get_user(message.from_user.id)

    if user:
        await message.answer(
            f"👤 <b>Profilingiz:</b>\n\n" # border qilish uchun 
            f"Ism: {user.full_name}\n" 
            f"Telefon: {user.phone}\n"
            f"Ro'yxatdan o'tgan: {user.created_at}",
            parse_mode="HTML" # o'sha holati ishlashi uchun shuni chaqirib qo'yammiz
        )
    else: # agar bazadan topolmasa o'zi avtomatik registratsiya qilishni so'raydi 
        await message.answer("Ismingizni kiriting:")
        await state.set_state(Register.name) # agar ismini kiritsa va kod. uni qabul qilsa , keyingi routerga o'tadi 

 
@router.message(Register.name) # ismini kiritdi, kod uni qabul qildi , endi keyingi actionni ya'ni telefon nomer kiritishni so'raydi
async def get_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer(
        "Telefon raqamingizni ulashing 👇",
        reply_markup=contact_menu
    )
    await state.set_state(Register.phone)


@router.message(Register.phone, F.contact)
async def get_phone(message: Message, state: FSMContext):
    data  = await state.get_data()
    name  = data["name"]
    phone = message.contact.phone_number
 # hamma kerakli ma'lumotlaar olingandan keyin bazaga saqlash boshlanadi ma'lumotlar kerakli ustunlarga taqqoslanadi
    await add_user(
        tg_id=message.from_user.id, # bu yerda callbackdan qaytgan aynan osha usrning maliumotlaridan telegrma idsini olib bazadagi tg_id ga saqlayd
        full_name=name, # boshida registratsiyada kiritgan ismini bazadagi full name ustuniga saqlaydi
        phone=phone  # registrdagi nomerni bazaga saqlaydi
    )
    logger.info(f"Ro'yxatdan o'tish yakunlandi | id={message.from_user.id}")

    await message.answer(
        f"✅ Ma'lumotlaringiz saqlandi!\n"
        f"Ism: {name}\n"
        f"Telefon: {phone}",
        reply_markup=main_menu
    )
    await state.clear() # xonada ishimizni qilib bo'lgandan keyin shu xonadan chqib ketish keyingi ishlar uchun boshqa xoanga kiriladi


@router.message(Register.phone, F.text == "❌ Bekor qilish")
async def cancel_register(message: Message, state: FSMContext):
    logger.info(f"Ro'yxatdan o'tish bekor qilindi | id={message.from_user.id}")
    await state.clear()
    await message.answer("Bekor qilindi.", reply_markup=main_menu)