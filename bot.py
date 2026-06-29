import asyncio 
from aiogram import Dispatcher, Bot
from config import BOT_TOKEN
from handlers import start, callback # kerakli ishga tushurish kerak bo'lgan handlersni chaqirganmiz



async def main():
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher() # bu direktor bo'lib routerlarni boshqaradi vazifalsi kerakli handlersni yo'naltirish
    dp.include_router(start.router) # bu yerda router handlarslarni yo'naltiradi vazifasi shu ya'ni menejer lekin dispatchersiz ishlamaydi
    dp.include_router(callback.router)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())