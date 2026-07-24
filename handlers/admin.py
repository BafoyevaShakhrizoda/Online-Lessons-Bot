from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from keyboards.admin_kb import (
    admin_menu, courses_admin_menu,
    cancel_kb, course_actions_kb, lesson_actions_kb
)
from utils.db.queries import (
    count_users, count_users_today,
    get_all_courses, get_course, add_course, update_course, delete_course,
    get_lessons_by_course, get_lesson, add_lesson, update_lesson, delete_lesson,
    get_all_users, count_enrollments_per_course,
     add_lesson_media, get_lesson_media, delete_lesson_media 
)
from utils.loggers import logger



from filters.admin_filter import IsAdmin  # filterdan chaqirib olganmiz 



router = Router()
router.message.filter(IsAdmin()) # agar adminlikka mos kelsa kerakli handlerslarga yo'naltir
router.callback_query.filter(IsAdmin()) # CRUD admin bo'lsa ruxsat ber




class AddCourse(StatesGroup):
    title       = State()
    description = State()


class EditCourse(StatesGroup):
    title       = State()
    description = State()


class AddLesson(StatesGroup):
    title     = State()
    content   = State()
    video_url = State()
    order     = State()


class EditLesson(StatesGroup):
    title     = State()
    content   = State()
    video_url = State()


class Broadcast(StatesGroup):
    message = State()



class AddMedia(StatesGroup):
    waiting_media = State()   # rasm/video/fayl/sticker kutilmoqda



@router.message(Command("admin"))# admin slashini bosganda  o'sha odamni idsini config id ilan tekshiradi 
async def cmd_admin(message: Message): 


    await message.answer("🔧 <b>Admin panel</b>", # idlarini mos kelsa shu yozuv qilib
                         reply_markup=admin_menu,
                         parse_mode="HTML")


@router.callback_query(F.data == "admin_back")  # bu birinchi marta bo'lma undan qolganlari bo'yicha  shu funksiya ishlab ketadi 
async def admin_back(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.answer("🔧 <b>Admin panel</b>",
                                  reply_markup=admin_menu,
                                  parse_mode="HTML")
    await callback.answer() 


@router.callback_query(F.data == "admin_cancel")
async def admin_cancel(callback: CallbackQuery, state: FSMContext):
    await state.clear() # o'chirib tashlasa
    await callback.message.answer("Bekor qilindi.",
                                  reply_markup=admin_menu) # o'sha vazifani qilishni bekor qilgan 
    await callback.answer()



@router.callback_query(F.data == "admin_stats")
async def show_stats(callback: CallbackQuery):
 

    total   = await count_users() # hammasini 
    today   = await count_users_today() # bugun qo'shilganlarni hammasi 
    courses = await count_enrollments_per_course() # qaysi kursdda nechta user borlini sanalgani

    course_stats = "\n".join(
        f"  • {c['title']}: {c['count']} ta o'quvchi"
        for c in courses
    ) or "  Kurslar yo'q"

    await callback.message.answer(
        f"📊 <b>Statistika:</b>\n\n"
        f"👥 Jami foydalanuvchilar: <b>{total}</b>\n"
        f"🆕 Bugun qo'shilganlar: <b>{today}</b>\n\n"
        f"📚 <b>Kurslar bo'yicha:</b>\n{course_stats}",
        parse_mode="HTML"
    )
    await callback.answer()



@router.callback_query(F.data == "admin_users")
async def show_users(callback: CallbackQuery):
  

    users = await get_all_users()

    if not users:
        await callback.message.answer("Hali hech kim ro'yxatdan o'tmagan.")
        await callback.answer()
        return

    text = "👥 <b>Foydalanuvchilar:</b>\n\n"
    for i, user in enumerate(users, start=1):
        text += (
            f"{i}. {user.full_name}\n"
            f"   📞 {user.phone}\n"
            f"   🆔 <code>{user.tg_id}</code>\n"
            f"   📅 {user.created_at.strftime('%d.%m.%Y')}\n\n"
        )

    await callback.message.answer(text, parse_mode="HTML")
    await callback.answer()



@router.callback_query(F.data == "admin_courses")
async def admin_courses(callback: CallbackQuery):


    await callback.message.answer("📚 <b>Kurslar boshqaruvi</b>",
                                  reply_markup=courses_admin_menu,
                                  parse_mode="HTML")
    await callback.answer()



@router.callback_query(F.data == "admin_list_courses") # bazada nechta kurs bo'lsa hammasini chiqarib berish 
async def list_courses_admin(callback: CallbackQuery):


    courses = await get_all_courses(only_active=False) # faqat active bo'lgan hamma kurslarni chiqarib beradi 

    if not courses:
        await callback.message.answer("Hozircha kurslar yo'q.",
                                      reply_markup=courses_admin_menu)
        await callback.answer()
        return

    from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(
                text=f"{'✅' if c.is_active else '❌'} {c.title}",
                callback_data=f"admin_course_{c.id}"
            )]
            for c in courses
        ] + [
            [InlineKeyboardButton(text="⬅️ Orqaga", callback_data="admin_courses")]
        ]
    )

    await callback.message.answer("📋 <b>Barcha kurslar:</b>",
                                  reply_markup=keyboard,
                                  parse_mode="HTML")
    await callback.answer()


@router.callback_query(F.data.startswith("admin_course_"))
async def course_detail_admin(callback: CallbackQuery): # kursni ichida qanaqa ma'luotlar bo'lsa shularni hammasini chiqarib berish 


    course_id = int(callback.data.split("_")[2])
    course    = await get_course(course_id) # bitta kursni ma'lumotlarini chiqarib ber 

    if not course:
        await callback.answer("Kurs topilmadi.", show_alert=True) # agar yo'q bo'lsa shu javob
        return

    await callback.message.answer(
        f"📘 <b>{course.title}</b>\n\n"
        f"{course.description}\n\n"
        f"Holati: {'✅ Aktiv' if course.is_active else '❌ Nofaol'}", #  kursni active yoki aktivmaasligigacha adminga chiqarib berish 
        reply_markup=course_actions_kb(course_id),
        parse_mode="HTML"
    )
    await callback.answer()



@router.callback_query(F.data == "admin_add_course") # admin kurs qo'shishi 
async def start_add_course(callback: CallbackQuery, state: FSMContext):
  
    await callback.message.answer("Kurs nomini kiriting:",# admindan kursni nomini kiritishni so'raydi 
                                  reply_markup=cancel_kb)
    await state.set_state(AddCourse.title)
    await callback.answer()


@router.message(AddCourse.title)  # agar title ni kiritib bo'lsagina keyin description kiritishni so'raydi 
async def add_course_title(message: Message, state: FSMContext):
    await state.update_data(title=message.text)
    await message.answer("Kurs tavsifini kiriting:", reply_markup=cancel_kb)
    await state.set_state(AddCourse.description) #agar bu bo'lsa keyin adminda describion kiritishni so'raydi 


@router.message(AddCourse.description) # ikkita ma'lumot qo'shilgandan keyin 
async def add_course_description(message: Message, state: FSMContext):
    data   = await state.get_data()
    course = await add_course(title=data["title"], description=message.text)

    await state.clear()
    await message.answer(
        f"✅ Kurs qo'shildi!\n\n"
        f"Nom: {course.title}\n"
        f"Tavsif: {course.description}",
        reply_markup=admin_menu
    ) # adminga shu ko'rinishda ko'rsatib beradi 



@router.callback_query(F.data.startswith("admin_edit_course_"))
async def start_edit_course(callback: CallbackQuery, state: FSMContext):
  

    course_id = int(callback.data.split("_")[3])
    await state.update_data(course_id=course_id)
    await callback.message.answer("Yangi kurs nomini kiriting:",
                                  reply_markup=cancel_kb)
    await state.set_state(EditCourse.title)
    await callback.answer()


@router.message(EditCourse.title)
async def edit_course_title(message: Message, state: FSMContext):
    await state.update_data(title=message.text)
    await message.answer("Yangi tavsifni kiriting:", reply_markup=cancel_kb)
    await state.set_state(EditCourse.description)


@router.message(EditCourse.description)
async def edit_course_description(message: Message, state: FSMContext):
    data = await state.get_data()
    await update_course(
        course_id=data["course_id"],
        title=data["title"],
        description=message.text
    )
    await state.clear()
    await message.answer("✅ Kurs yangilandi!", reply_markup=admin_menu)



@router.callback_query(F.data.startswith("admin_delete_course_"))
async def confirm_delete_course(callback: CallbackQuery):


    course_id = int(callback.data.split("_")[3])
    course    = await get_course(course_id)

    from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
    confirm_kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(
                text="✅ Ha, o'chir",
                callback_data=f"admin_confirm_delete_course_{course_id}"
            )],
            [InlineKeyboardButton(text="❌ Yo'q", callback_data="admin_list_courses")],
        ]
    )

    await callback.message.answer(
        f"⚠️ <b>{course.title}</b> kursini o'chirishni tasdiqlaysizmi?\n"
        f"Barcha darslar ham o'chib ketadi!",
        reply_markup=confirm_kb,
        parse_mode="HTML"
    )
    await callback.answer()


@router.callback_query(F.data.startswith("admin_confirm_delete_course_"))
async def do_delete_course(callback: CallbackQuery):
    course_id = int(callback.data.split("_")[4])
    await delete_course(course_id)
    await callback.message.answer("✅ Kurs o'chirildi.", reply_markup=admin_menu)
    await callback.answer()


@router.callback_query(F.data.startswith("admin_lessons_"))
async def list_lessons_admin(callback: CallbackQuery):

    course_id = int(callback.data.split("_")[2]) #  aynan shu darslar o'sha kursga tegishliligini tekshirish 
    lessons   = await get_lessons_by_course(course_id)

    if not lessons:
        await callback.message.answer(
            "Bu kursda hali darslar yo'q.",
            reply_markup=course_actions_kb(course_id)
        )
        await callback.answer()
        return

    from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(
                text=f"{lesson.order}. {lesson.title}",
                callback_data=f"admin_lesson_{lesson.id}_{course_id}"
            )]
            for lesson in lessons
        ] + [
            [InlineKeyboardButton(
                text="⬅️ Orqaga",
                callback_data=f"admin_course_{course_id}"
            )]
        ]
    )

    await callback.message.answer("📋 <b>Darslar ro'yxati:</b>",
                                  reply_markup=keyboard,
                                  parse_mode="HTML")
    await callback.answer()


@router.callback_query(F.data.startswith("admin_lesson_"))
async def lesson_detail_admin(callback: CallbackQuery):
    parts     = callback.data.split("_")
    lesson_id = int(parts[2])
    course_id = int(parts[3])
    lesson    = await get_lesson(lesson_id)

    await callback.message.answer(
        f"📖 <b>{lesson.title}</b>\n\n"
        f"{lesson.content or 'Kontent yo\'q'}\n\n"
        f"🎥 Video: {lesson.video_url or 'Yo\'q'}\n"
        f"Tartib: {lesson.order}",
        reply_markup=lesson_actions_kb(lesson_id, course_id),
        parse_mode="HTML"
    )
    await callback.answer()



@router.callback_query(F.data.startswith("admin_add_lesson_"))
async def start_add_lesson(callback: CallbackQuery, state: FSMContext):


    course_id = int(callback.data.split("_")[3])
    await state.update_data(course_id=course_id)
    await callback.message.answer("Dars nomini kiriting:", reply_markup=cancel_kb)
    await state.set_state(AddLesson.title)
    await callback.answer()


@router.message(AddLesson.title)
async def add_lesson_title(message: Message, state: FSMContext):
    await state.update_data(title=message.text)
    await message.answer("Dars matnini kiriting:", reply_markup=cancel_kb)
    await state.set_state(AddLesson.content)


@router.message(AddLesson.content)
async def add_lesson_content(message: Message, state: FSMContext):
    await state.update_data(content=message.text)
    await message.answer(
        "Video URL ni kiriting:\n(Yo'q bo'lsa — 'yo'q' deb yozing)",
        reply_markup=cancel_kb
    )
    await state.set_state(AddLesson.video_url)


@router.message(AddLesson.video_url)
async def add_lesson_video(message: Message, state: FSMContext):
    video_url = None if message.text.lower() == "yo'q" else message.text
    await state.update_data(video_url=video_url)
    await message.answer("Dars tartib raqamini kiriting (1, 2, 3...):",
                         reply_markup=cancel_kb)
    await state.set_state(AddLesson.order)


@router.message(AddLesson.order)
async def add_lesson_order(message: Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("Raqam kiriting:")
        return

    data   = await state.get_data()
    lesson = await add_lesson(
        course_id=data["course_id"],
        title=data["title"],
        content=data["content"],
        video_url=data["video_url"],
        order=int(message.text)
    )

    await state.clear()
    await message.answer(
        f"✅ Dars qo'shildi!\n\n"
        f"Nom: {lesson.title}\n"
        f"Tartib: {lesson.order}",
        reply_markup=admin_menu
    )



@router.callback_query(F.data.startswith("admin_edit_lesson_"))
async def start_edit_lesson(callback: CallbackQuery, state: FSMContext):


    lesson_id = int(callback.data.split("_")[3])
    await state.update_data(lesson_id=lesson_id)
    await callback.message.answer("Yangi dars nomini kiriting:",
                                  reply_markup=cancel_kb)
    await state.set_state(EditLesson.title)
    await callback.answer()


@router.message(EditLesson.title)
async def edit_lesson_title(message: Message, state: FSMContext):
    await state.update_data(title=message.text)
    await message.answer("Yangi dars matnini kiriting:", reply_markup=cancel_kb)
    await state.set_state(EditLesson.content)


@router.message(EditLesson.content)
async def edit_lesson_content(message: Message, state: FSMContext):
    await state.update_data(content=message.text)
    await message.answer(
        "Yangi video URL kiriting:\n(Yo'q bo'lsa — 'yo'q' deb yozing)",
        reply_markup=cancel_kb
    )
    await state.set_state(EditLesson.video_url)


@router.message(EditLesson.video_url)
async def edit_lesson_video(message: Message, state: FSMContext):
    data      = await state.get_data()
    video_url = None if message.text.lower() == "yo'q" else message.text

    await update_lesson(
        lesson_id=data["lesson_id"],
        title=data["title"],
        content=data["content"],
        video_url=video_url
    )
    await state.clear()
    await message.answer("✅ Dars yangilandi!", reply_markup=admin_menu)



@router.callback_query(F.data.startswith("admin_delete_lesson_"))
async def do_delete_lesson(callback: CallbackQuery):


    lesson_id = int(callback.data.split("_")[3])
    await delete_lesson(lesson_id)
    await callback.message.answer("✅ Dars o'chirildi.", reply_markup=admin_menu)
    await callback.answer()




@router.callback_query(F.data == "admin_broadcast") # admin qanaqadur message yozadi u botga start bosgan hammaga koriniadi 
async def start_broadcast(callback: CallbackQuery, state: FSMContext):


    await callback.message.answer("📢 Yubormoqchi bo'lgan xabaringizni yozing:",
                                  reply_markup=cancel_kb)
    await state.set_state(Broadcast.message)
    await callback.answer()


@router.message(Broadcast.message)
async def send_broadcast(message: Message, state: FSMContext):


    users   = await get_all_users()
    success = 0
    failed  = 0

    for user in users:
        try:
            await message.copy_to(chat_id=user.tg_id)
            success += 1
        except Exception as e:
            failed += 1
            logger.error(f"Broadcast xatosi | id={user.tg_id} | {e}")

    await state.clear()
    await message.answer(
        f"✅ Broadcast yakunlandi!\n\n"
        f"Yuborildi: {success}\n"
        f"Xato: {failed}",
        reply_markup=admin_menu
    )
    logger.info(f"Broadcast | muvaffaqiyatli={success} | xato={failed}")
    
    
 
 
 
 
 
 
 
 
    
    

# Media qo'shish — tugma bosilganda
@router.callback_query(F.data.startswith("admin_add_media_"))
async def start_add_media(callback: CallbackQuery, state: FSMContext):
    lesson_id = int(callback.data.split("_")[3])
    await state.update_data(lesson_id=lesson_id)

    await callback.message.answer(
        "📎 Media yuboring:\n\n"
        "🖼 Rasm\n"
        "🎥 Video\n"
        "📄 Fayl (document)\n"
        "😀 Sticker\n\n"
        "Istalgan turini yuboring 👇",
        reply_markup=cancel_kb
    )
    await state.set_state(AddMedia.waiting_media)
    await callback.answer()


# Rasm keldi
@router.message(AddMedia.waiting_media, F.photo)
async def add_media_photo(message: Message, state: FSMContext):
    data      = await state.get_data()
    lesson_id = data["lesson_id"]
    photo     = message.photo[-1]   # eng yuqori sifat

    await add_lesson_media(
        lesson_id=lesson_id,
        media_type="photo",
        file_id=photo.file_id,
        caption=message.caption
    )
    await state.clear()
    await message.answer("✅ Rasm darsga qo'shildi!", reply_markup=admin_menu)


# Video keldi
@router.message(AddMedia.waiting_media, F.video)
async def add_media_video(message: Message, state: FSMContext):
    data      = await state.get_data()
    lesson_id = data["lesson_id"]

    await add_lesson_media(
        lesson_id=lesson_id,
        media_type="video",
        file_id=message.video.file_id,
        caption=message.caption
    )
    await state.clear()
    await message.answer("✅ Video darsga qo'shildi!", reply_markup=admin_menu)


# Fayl keldi
@router.message(AddMedia.waiting_media, F.document)
async def add_media_document(message: Message, state: FSMContext):
    data      = await state.get_data()
    lesson_id = data["lesson_id"]

    await add_lesson_media(
        lesson_id=lesson_id,
        media_type="document",
        file_id=message.document.file_id,
        caption=message.caption or message.document.file_name
    )
    await state.clear()
    await message.answer("✅ Fayl darsga qo'shildi!", reply_markup=admin_menu)


# Sticker keldi
@router.message(AddMedia.waiting_media, F.sticker)
async def add_media_sticker(message: Message, state: FSMContext):
    data      = await state.get_data()
    lesson_id = data["lesson_id"]

    await add_lesson_media(
        lesson_id=lesson_id,
        media_type="sticker",
        file_id=message.sticker.file_id,
        caption=None
    )
    await state.clear()
    await message.answer("✅ Sticker darsga qo'shildi!", reply_markup=admin_menu)


# Media ro'yxati — admin ko'rish va o'chirish uchun
@router.callback_query(F.data.startswith("admin_media_list_"))
async def show_media_list(callback: CallbackQuery):
    parts     = callback.data.split("_")
    lesson_id = int(parts[3])
    course_id = int(parts[4])
    media_list = await get_lesson_media(lesson_id)

    if not media_list:
        await callback.message.answer(
            "Bu darsda hali media yo'q.",
            reply_markup=lesson_actions_kb(lesson_id, course_id)
        )
        await callback.answer()
        return

    # Har bir mediaga o'chirish tugmasi
    from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
    buttons = []
    for m in media_list:
        icon = {"photo": "🖼", "video": "🎥",
                "document": "📄", "sticker": "😀"}.get(m.media_type, "📎")
        buttons.append([
            InlineKeyboardButton(
                text=f"{icon} {m.media_type} | {m.caption or 'caption yo\'q'}",
                callback_data=f"admin_delete_media_{m.id}_{lesson_id}_{course_id}"
            )
        ])

    buttons.append([
        InlineKeyboardButton(
            text="⬅️ Orqaga",
            callback_data=f"admin_lesson_{lesson_id}_{course_id}"
        )
    ])

    await callback.message.answer(
        f"📎 <b>Dars medialari ({len(media_list)} ta):</b>\n"
        "O'chirish uchun bosing 👇",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons),
        parse_mode="HTML"
    )
    await callback.answer()


# Media o'chirish
@router.callback_query(F.data.startswith("admin_delete_media_"))
async def delete_media(callback: CallbackQuery):
    parts     = callback.data.split("_")
    media_id  = int(parts[3])
    lesson_id = int(parts[4])
    course_id = int(parts[5])

    await delete_lesson_media(media_id)
    await callback.message.answer(
        "✅ Media o'chirildi.",
        reply_markup=lesson_actions_kb(lesson_id, course_id)
    )
    await callback.answer()
