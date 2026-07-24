from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine
)
from config import DB_URL
from utils.loggers import logger
from utils.db.models import Base
from sqlalchemy import text


# databazani ulash uchun doimiy ishlatiladigan engine
engine = create_async_engine( 
    url=DB_URL,
    echo=False,   
)# terminalda databaza yaratganigni natijasini chiqarma

AsyncSessionLocal = async_sessionmaker(
    bind=engine, # databaza ulandimi 
    class_=AsyncSession, #  ishga tushirgandan boshlab bo'lgan actionlar
    expire_on_commit=False   # commit dan keyin ma'lumotlar yo'qolmasin
)


async def create_tables(): # tranzaksiya faqat moliyaviy masalalr uchun kelmagan 
    async with engine.begin() as conn: # tranzakiya boshlanishi  
        await conn.run_sync(Base.metadata.create_all) # python code orqali hammasini jadval ko'rinishida emas shunchaki chiqarish uchun chaqirilgan
        logger.info("Jadvallar yaratildi ") # terminalda response qaytadi jadval yaratildi 


async def close_engine(): # close engine degani bazaga ulanishni toxtatish degani
    await engine.dispose()  # toxtatish funksiyasi
    logger.info("DB ulanishi yopildi ") # response sifatida qaytadigan javob
    
    
    # -> men qanaqadyr request jonatdim ( yangi user yaratdim) -> bazangga qo'shib qo'y(request)
    # -> qnadaydur response ( ya'ni bazasiga saqlab qo'yganini menga bildirishi kerak) -> qo'shib qo'ydim(response)

async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

        # Mavjud jadvalga yangi ustun qo'shish (agar yo'q bo'lsa)
        await conn.execute(text("""
            ALTER TABLE users 
            ADD COLUMN IF NOT EXISTS is_blocked BOOLEAN DEFAULT FALSE
        """))
        await conn.execute(text("""
            ALTER TABLE users 
            ADD COLUMN IF NOT EXISTS language VARCHAR(10) DEFAULT 'uz'
        """))
        logger.info("Jadvallar yaratildi ✅")
