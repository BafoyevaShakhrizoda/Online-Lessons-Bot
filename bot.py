import asyncio
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from config import BOT_TOKEN
from utils.loggers import logger
from utils.db.database import create_tables, close_engine

from middlewares.logger_middleware import LoggerMiddleware
from middlewares.throttling_middleware import ThrottlingMiddleware
from middlewares.i18n_middlewares import I18nMiddleware

from handlers import start, register, profile, courses, admin, help
from aiogram.types import BotCommand


async def main():
    logger.info("=" * 40)
    logger.info("Bot ishga tushmoqda...")

    await create_tables()

    bot = Bot(token=BOT_TOKEN)
    dp  = Dispatcher(storage=MemoryStorage())

    # Bot buyruqlari va tavsifini o'rnatish
    await bot.set_my_commands([
        BotCommand(command="start", description="Ishga tushirish / Запуск / Start"),
        BotCommand(command="help", description="Yordam / Помощь / Help")
    ])

    await bot.set_my_description(
        description="Online Lessons Bot — bu bot orqali siz darslar va media materiallarni ko'rishingiz hamda kurslarga a'zo bo'lishingiz mumkin. Boshlash uchun /start tugmasini bosing.",
        language_code="uz"
    )
    await bot.set_my_description(
        description="Online Lessons Bot — с помощью этого бота вы можете просматривать уроки, медиаматериалы и записываться на курсы. Нажмите /start для запуска.",
        language_code="ru"
    )
    await bot.set_my_description(
        description="Online Lessons Bot — here you can view lessons and media materials, and enroll in courses. Click /start to begin.",
        language_code="en"
    )

    # Middlewarelar — tartib muhim!
    dp.message.middleware(LoggerMiddleware())
    dp.message.middleware(ThrottlingMiddleware(rate_limit=1.0))
    dp.message.middleware(I18nMiddleware())
    dp.callback_query.middleware(I18nMiddleware())

    # Routerlar — tartib muhim!
    dp.include_router(start.router)    # /start
    dp.include_router(register.router) # ro'yxatdan o'tish (FSM)
    dp.include_router(profile.router)  # 👤 Profil
    dp.include_router(courses.router)  # 📚 Kurslar + darslar + media
    dp.include_router(help.router)     # ℹ️ Yordam (/help)
    dp.include_router(admin.router)    # /admin panel

    logger.info("Barcha routerlar ulandi ✅")
    logger.info("Polling boshlandi ✅")
    logger.info("=" * 40)

    try:
        await dp.start_polling(bot)
    finally:
        await close_engine()
        logger.info("Bot to'xtatildi")


if __name__ == "__main__":
    asyncio.run(main())