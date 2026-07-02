from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext #Ketma ketlikda beriladigan savollar xuddi profil ma'lumotlarni to'ldirishdek
from aiogram.fsm.state import State, StatesGroup 
from keyboards.reply import main_menu, contact_menu # bu joyida asosiy menyu bilan telefonni ulashishni buttonlarini import qildik

router = Router()

class Register(StatesGroup): # qanaqa savollar berishingizni ketma ketlikda yozib ketish uchun kerak 
    name  = State()    # bularni hammasi bir xil = State() bo'ladi faqat savollarni nomlarini to'g'ri ketmaketlikda yozish kerak
    phone = State() 
    # age = State() 
    # email = State() 

@router.message(F.text == "👤 Profil") # bitta state tugaganidan keyin keyingisi ishlab ketadi
async def start_register(message: Message, state: FSMContext):
    await message.answer("Ismingizni kiriting:")
    await state.set_state(Register.name)


# statelarda nima bo'lsa router kodlar ham shu ketma ketlikda bo'ladi
@router.message(Register.name)
async def get_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer(
        "Telefon raqamingizni ulashing 👇",
        reply_markup=contact_menu # shu joyida reply dan contact button ya'ni telefon raqamni ulashish buttoni chaqirilgan
    )
    await state.set_state(Register.phone)

@router.message(Register.phone, F.contact) # button bosilgandan keyin userni raqamini oladi
async def get_phone(message: Message, state: FSMContext):
    data = await state.get_data()
    name  = data["name"]
    phone = message.contact.phone_number

    await message.answer(
        f" Ma'lumotlaringiz:\n"
        f"Ism: {name}\n"
        f"Telefon: {phone}",
        reply_markup=main_menu   
    )# kerakli ma'lumotlarni kiritgandan keyin userga xabar sifatida ko'rsatadi
    await state.clear() # state'larni tozalash , state'lar o'z ishini tugatganidan keyin tozalandi

@router.message(Register.phone, F.text == "Bekor qilish") # shu joyida reply dagi buttonlar bilan bir xil ekanligiga e'tibor berish kerak 
async def cancel_register(message: Message, state: FSMContext):
    await state.clear() # qachonki statelarimiz tugasa oxirida tozalsh uchun clear qilish kerak ya'ni tozalash kerak
    await message.answer("Bekor qilindi.", reply_markup=main_menu) # javob qaytarishi bilan asosiy menu'ni ko'rsatgan 