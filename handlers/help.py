from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message
from utils.i18n import _

router = Router()

@router.message(Command("help"))
@router.message(F.text.in_({"ℹ️ Yordam", "ℹ️ Помощь", "ℹ️ Help"}))
async def help_command(message: Message, lang: str = "uz"):
    help_texts = {
        "uz": (
            "🤖 <b>Bot Yordam Bo'limi</b>\n\n"
            "Ushbu bot orqali siz darslarni o'rganishingiz va darslik materiallarini ko'rishingiz mumkin.\n\n"
            "📌 <b>Asosiy buyruqlar:</b>\n"
            "/start - Botni qayta ishga tushirish\n"
            "/help - Yordam xabarini ko'rsatish\n\n"
            "📂 <b>Menyu bo'limlari:</b>\n"
            "👤 Profil - Profil ma'lumotlari va yozilgan kurslaringiz\n"
            "📚 Kurslar - Mavjud kurslar ro'yxati va darsliklar\n"
            "ℹ️ Yordam - Qo'llab-quvvatlash xizmati\n\n"
            "📞 Savollar yoki muammolar bo'lsa: @Shahrizoda_Bafoyeva"
        ),
        "ru": (
            "🤖 <b>Раздел помощи бота</b>\n\n"
            "С помощью этого бота вы можете изучать курсы и просматривать учебные материалы.\n\n"
            "📌 <b>Основные команды:</b>\n"
            "/start - Перезапустить бота\n"
            "/help - Показать справочную информацию\n\n"
            "📂 <b>Разделы меню:</b>\n"
            "👤 Профиль - Данные вашего профиля и ваши курсы\n"
            "📚 Курсы - Список доступных курсов и уроков\n"
            "ℹ️ Помощь - Служба поддержки\n\n"
            "📞 По всем вопросам: @Shahrizoda_Bafoyeva"
        ),
        "en": (
            "🤖 <b>Bot Help Section</b>\n\n"
            "Through this bot, you can study courses and view educational materials.\n\n"
            "📌 <b>Main Commands:</b>\n"
            "/start - Restart the bot\n"
            "/help - Show help information\n\n"
            "📂 <b>Menu Sections:</b>\n"
            "👤 Profile - Your profile details and enrolled courses\n"
            "📚 Courses - List of available courses and lessons\n"
            "ℹ️ Help - Support service\n\n"
            "📞 For any questions or support: @Shahrizoda_Bafoyeva"
        )
    }
    await message.answer(help_texts.get(lang, help_texts["uz"]), parse_mode="HTML")
