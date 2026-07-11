from sqlalchemy import select, delete, update, func # o'sha select 
from sqlalchemy.dialects.postgresql import insert # o'sha insert
from utils.db.database import AsyncSessionLocal # databazaga ulangandan keyin chaqirilgan
from utils.db.models import User,Lesson,Course,Enrollment # databazani ichida yaratilgan table chaqirlgan
from utils.loggers import logger # shu file ni ichida kodlar qay holatda ishlasa shuni hammasini formatlab yozib boradi
from datetime import datetime



async def add_user(tg_id: int, full_name: str, phone: str):
    async with AsyncSessionLocal() as session: # xuddi get connectionni chaqirgandek chaqirilgan 
        stmt = insert(User).values(
            tg_id=tg_id,
            full_name=full_name,
            phone=phone #. insert into table values (ali, vali)
        ).on_conflict_do_nothing(index_elements=["tg_id"]) # databazaga registratsiya qilgan usetni qo'sh agar o'sha bo'lsa xatolik berma

        await session.execute(stmt)
        await session.commit()
        logger.info(f"Foydalanuvchi saqlandi | id={tg_id} | ism={full_name}")

# select * from users where id = { siz soragan id};
async def get_user(tg_id: int) -> User | None: # agar bazada bo'lsa datalarni qaytaradi bo'lmasa None
    async with AsyncSessionLocal() as session: # databazaga ulash 
        result = await session.execute(
            select(User).where(User.tg_id == tg_id) # siz so'ragan userni idsini bazadagi idlar bilan solishtirib chiqadi
        )
        user = result.scalar_one_or_none() # magar mavjud bo'lsa 1 tas chiqar bo'lmasa yo'q 
        if user:
            logger.debug(f"Foydalanuvchi topildi | id={tg_id}")
        else:
            logger.debug(f"Foydalanuvchi topilmadi | id={tg_id}")
        return user # return orqali yoki none yoki o'sha user chiqadi
 

async def get_all_users() -> list[User]: # select * from users;
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(User)) # o'sha tableni belgilayapti
        return result.scalars().all() #  belgilangan table dagi hammasi ol bazada bor 


async def delete_user(tg_id: int): # delete from users where id == [SIZ SORAGAN ID]
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(User).where(User.tg_id == tg_id) # ochirmoqchi bolgan odamingni id si bo'yicha izla
        )
        user = result.scalar_one_or_none() # yoki natija 1 ta bo'ladi yoki none bo'ladi 
        if user: # agar natija 1ta bo'lsa o'chirib tashlab commit qil 
            await session.delete(user)
            await session.commit()
            logger.info(f"Foydalanuvchi o'chirildi | id={tg_id}") # osha ochirilgan odamni yozib qo'y
            

# YANGILANGAN KODLAR YA'NI YANGI QO'SHILGAN KODLAR 


async def count_users() -> int: # databazada bor userlarni sanab beradi
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(func.count()).select_from(User)
        )
        return result.scalar()


async def count_users_today() -> int:
    async with AsyncSessionLocal() as session:
        today = datetime.now().date()
        result = await session.execute(
            select(func.count()).select_from(User).where(
                func.date(User.created_at) == today
            )
        )
        return result.scalar()
 # bugun databazaga qancha odam qo'shilganini sanab beradi 



# endi keyingi sectionga ya'ni user haqidagi tugagan bo'lsa. darslarni sectioniga o'tishimiz kk ya'ni kurs sectionida CRUD amallar

async def add_course(title: str, description: str) -> Course: # admin kurs  databazaga qo'shishi uchun
    async with AsyncSessionLocal() as session: 
        course = Course(title=title, description=description)
        session.add(course)
        await session.commit()
        await session.refresh(course)
        logger.info(f"Yangi kurs qo'shildi | {title}")
        return course


async def get_all_courses(only_active: bool = True) -> list[Course]: # admin bazasida bor hamma kursni ko'rishi uchun 
    async with AsyncSessionLocal() as session:
        query = select(Course) # so'rov sifatida kurs chaqirilgan 
        if only_active: # faqat active bo'lgan kurslarni adminga ko'rsatadi
            query = query.where(Course.is_active == True) # shartida active bo'lgan kurslarni chaqirgan 
        result = await session.execute(query) # natijasini chiqarib berish 
        return result.scalars().all() # hammasini chiqarib berish 

async def get_course(course_id: int) -> Course | None: # bitta kursni ko'rish 
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(Course).where(Course.id == course_id) # admin kiritadigan id bazadagi id ga mos kelsa kursni chiqaradi kelmasa none qaytaradi
        )
        return result.scalar_one_or_none() # yiki bitta chiqar yoki none chiqar


async def update_course(course_id: int, title: str, description: str): # kursni tahrirlash 
    async with AsyncSessionLocal() as session:
        await session.execute(
            update(Course)
            .where(Course.id == course_id) # admin kiritadigan id ga mos kelsa 
            .values(title=title, description=description) # shu ikkalasini course table'idan yani bazadan yangila
        )
        await session.commit() # bu joyda bazaga saqlagan hamda log sifatid ayozib ketgan
        logger.info(f"Kurs yangilandi | id={course_id}")


async def delete_course(course_id: int): # bu yerda courselarni bazadan o'chirib tashlash 
    async with AsyncSessionLocal() as session:
        await session.execute(
            delete(Course).where(Course.id == course_id) # id bazadagi id ga mos kelsa o'chirib tashla
        )
        await session.commit()
        logger.info(f"Kurs o'chirildi | id={course_id}")


async def count_enrollments_per_course() -> list[dict]:
    # Har bir kursda nechta o'quvchi borligini qaytaradi
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(Course.title, func.count(Enrollment.id).label("count")) # count band qilinganlarni id si bo'yicha sanaydi 
            .join(Enrollment, Enrollment.course_id == Course.id, isouter=True) # 2 ta tableni birlashtirib qaysi kursda qancha enrolment bo'lganini sanab beradi ya'ni qaysi kursda nechta user bor shuni sanaydi
            .group_by(Course.id) # kurshar bir kurs uchun alohida sanagan ya'ni har bitta kurs gruppalangan
        )
        return [{"title": row[0], "count": row[1]} for row in result.all()] # hammasini nomi va nechta userlari borligini sonini adminga qaytaradi 
    
    


# endi kurslar sectioni darsni ko'ramiz 

async def add_lesson(course_id: int, title: str, content: str,# aynan mos kelgan darsni kursga bo'glaganmiz
                     video_url: str, order: int) -> Lesson:
    async with AsyncSessionLocal() as session:
        lesson = Lesson(
            course_id=course_id,
            title=title,
            content=content,
            video_url=video_url,
            order=order
        )# hammasini admin qo'lda kiritib chiqadi biz kod bilan yozishimiz shart emas 
        session.add(lesson) # admin kiritgan ma'lumotlar lessonga qo'shiladi 
        await session.commit() # keyin u bazaga saqlanadi
        await session.refresh(lesson) # bazani bitta yangilab yuborib
        logger.info(f"Yangi dars qo'shildi | kurs={course_id} | {title}") # bu yerida loglarini shu formatda yozib beradi 
        return lesson 

async def get_lessons_by_course(course_id: int) -> list[Lesson]: # kursni bossa o'shanga tegishli bo'lgan hamma darslarni chiqarib beradi , shuning uchun biz join bilan ikkkila table birlashtirilgan 
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(Lesson) 
            .where(Lesson.course_id == course_id)# buyoqda sqldagi joinlarni logikasi ketgan lessonlarni courselarga moslarini tenglashtganmiz
            .order_by(Lesson.order) # tartiblab chiqarish 
        )
        return result.scalars().all() # hammasini chiqarish 


async def get_lesson(lesson_id: int) -> Lesson | None: 
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(Lesson).where(Lesson.id == lesson_id)
        )
        return result.scalar_one_or_none()

async def update_lesson(lesson_id: int, title: str,
                        content: str, video_url: str):
    async with AsyncSessionLocal() as session:
        await session.execute(
            update(Lesson)
            .where(Lesson.id == lesson_id)
            .values(title=title, content=content, video_url=video_url)
        )
        await session.commit()
        logger.info(f"Dars yangilandi | id={lesson_id}")


async def delete_lesson(lesson_id: int):
    async with AsyncSessionLocal() as session:
        await session.execute(
            delete(Lesson).where(Lesson.id == lesson_id)
        )
        await session.commit()
        logger.info(f"Dars o'chirildi | id={lesson_id}")

# lessons bo'lgandan keyin nedi enrollmentni ko'ramiz

async def enroll_user(user_id: int, course_id: int):# modelsda 3 ta table'dagi mos qiymatlar  birlashtirilgandi 
    async with AsyncSessionLocal() as session:
        # Avval yozilganmi tekshiramiz
        result = await session.execute(
            select(Enrollment).where(
                Enrollment.user_id == user_id, # avval band qilgan odamni bazada borligini izlaydi 
                Enrollment.course_id == course_id # user kiritgan coursni ro'stdanam band qilganmi yoqmi tekshiradi 
            )
        )
        if result.scalar_one_or_none():
            return False   # allaqachon yozilgan
        
        enrollment = Enrollment(user_id=user_id, course_id=course_id)
        session.add(enrollment) # shu olgan ma'lumotlarimizni enrollmentda qo'shgan 
        await session.commit() # keyin esa bazaga save qilgan 
        logger.info(f"Kursga yozildi | user={user_id} | kurs={course_id}")
        return True


async def get_user_courses(user_id: int) -> list[Course]: # user qaysi kurslarni band qilgan shuni ko'rish 
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(Course) # 2 ta jadvalni birlashtir
            .join(Enrollment, Enrollment.course_id == Course.id) # ikkita jadvalda mos kelgan kurslarni oladi 
            .where(Enrollment.user_id == user_id) # undan keyin enrolment bilan userni ma'lumotlari mmos kelganini oladi shunda o'sha user qaysi qaysi kurslarda o'qiyotgani chiqadi
        )
        return result.scalars().all() # user band qilgan hamma kurslarni chiqar