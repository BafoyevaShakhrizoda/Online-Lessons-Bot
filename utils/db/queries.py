from sqlalchemy import select # o'sha select 
from sqlalchemy.dialects.postgresql import insert # o'sha insert
from utils.db.database import AsyncSessionLocal # databazaga ulangandan keyin chaqirilgan
from utils.db.models import User # databazani ichida yaratilgan table chaqirlgan
from utils.loggers import logger # shu file ni ichida kodlar qay holatda ishlasa shuni hammasini formatlab yozib boradi




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
            





