import os
import struct

TRANSLATIONS = {
    "uz": {
        "welcome":          "Xush kelibsiz, {name}! 👋",
        "courses":          "📚 Mavjud kurslar",
        "profile":          "👤 Profilingiz",
        "no_courses":       "Hozircha kurslar mavjud emas.",
        "enrolled":         "✅ Kursga yozildingiz!",
        "already_enrolled": "Siz allaqachon yozilgansiz.",
        "register_name":    "Ismingizni kiriting:",
        "register_phone":   "Telefon raqamingizni ulashing 👇",
        "register_done":    "✅ Ro'yxatdan o'tdingiz!",
        "cancelled":        "Bekor qilindi.",
        "no_permission":    "⛔ Sizda ruxsat yo'q.",
        "no_lessons":       "Bu kursda hali darslar yo'q.",
        "lesson_done":      "✅ Dars materiallari yuborildi!",
    },
    "ru": {
        "welcome":          "Добро пожаловать, {name}! 👋",
        "courses":          "📚 Доступные курсы",
        "profile":          "👤 Ваш профиль",
        "no_courses":       "Пока курсов нет.",
        "enrolled":         "✅ Вы записались на курс!",
        "already_enrolled": "Вы уже записаны.",
        "register_name":    "Введите ваше имя:",
        "register_phone":   "Поделитесь номером телефона 👇",
        "register_done":    "✅ Вы зарегистрированы!",
        "cancelled":        "Отменено.",
        "no_permission":    "⛔ У вас нет доступа.",
        "no_lessons":       "В этом курсе пока нет уроков.",
        "lesson_done":      "✅ Материалы урока отправлены!",
    },
    "en": {
        "welcome":          "Welcome, {name}! 👋",
        "courses":          "📚 Available courses",
        "profile":          "👤 Your profile",
        "no_courses":       "No courses available yet.",
        "enrolled":         "✅ Successfully enrolled!",
        "already_enrolled": "You are already enrolled.",
        "register_name":    "Enter your name:",
        "register_phone":   "Share your phone number 👇",
        "register_done":    "✅ Registration complete!",
        "cancelled":        "Cancelled.",
        "no_permission":    "⛔ You don't have permission.",
        "no_lessons":       "No lessons in this course yet.",
        "lesson_done":      "✅ Lesson materials sent!",
    }
}


def create_mo_file(translations: dict, path: str): # dict = dictionary = { key: values} dict= { 'moshina': 'Chevrolet'}
    keys   = sorted(translations.keys()) # bu kalitlar aynan nimani tarjima qilishi
    values = [translations[k] for k in keys] # o'sha kalitlarga mos qiladigan qiymatlarni chiqarishi ya'ni tarjima qilishini so'ragan 
# kalit ham qiynat ham kampyuter tilidan oddiy  odam oqiy oladigan tilga o'girilgan 
    keys_encoded   = [k.encode("utf-8") for k in keys]
    values_encoded = [v.encode("utf-8") for v in values]

    n   = len(keys)
    offsets = []
    current = 28 + 16 * n

    for k in keys_encoded:
        offsets.append((len(k), current))
        current += len(k) + 1

    val_offsets = []
    for v in values_encoded:
        val_offsets.append((len(v), current))
        current += len(v) + 1

    output  = struct.pack("<I", 0x950412de)
    output += struct.pack("<I", 0)
    output += struct.pack("<I", n)
    output += struct.pack("<I", 28)
    output += struct.pack("<I", 28 + 8 * n)
    output += struct.pack("<I", 0)
    output += struct.pack("<I", 0)

    for length, offset in offsets:
        output += struct.pack("<II", length, offset)
    for length, offset in val_offsets:
        output += struct.pack("<II", length, offset)
    for k in keys_encoded:
        output += k + b"\x00"
    for v in values_encoded:
        output += v + b"\x00"

    with open(path, "wb") as f:
        f.write(output)


def setup():
    for lang, translations in TRANSLATIONS.items():
        folder  = os.path.join("locales", lang, "LC_MESSAGES")
        os.makedirs(folder, exist_ok=True)
        print(f"📁 Papka: {folder}")

        po_path = os.path.join(folder, "bot.po")
        with open(po_path, "w", encoding="utf-8") as f:
            f.write('msgid ""\nmsgstr ""\n')
            f.write('"Content-Type: text/plain; charset=UTF-8\\n"\n\n')
            for key, value in translations.items():
                f.write(f'msgid "{key}"\n')
                f.write(f'msgstr "{value}"\n\n')
        print(f"✅ .po: {po_path}")

        mo_path = os.path.join(folder, "bot.mo")
        create_mo_file(translations, mo_path)
        print(f"✅ .mo: {mo_path}")

    print("\n🎉 Locales tayyor!")


if __name__ == "__main__":
    setup()

