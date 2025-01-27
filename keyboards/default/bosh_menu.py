from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def admin_reply_buttons():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)

    buttons = [
        KeyboardButton("Users 👥"),
        KeyboardButton("Channel Settings ⚙️"),
        KeyboardButton("Statistika 📊"),
        KeyboardButton("Announcement 📢"),

    ]

    markup.add(*buttons)
    return markup

def user_reply_buttons():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)

    buttons = [
        KeyboardButton("🔗 Referal"),
        KeyboardButton("Statistika 📊"),
        KeyboardButton(text="✉️ Murojaat"),
        KeyboardButton(text="📊 Mening natijalarim"),

    ]

    markup.add(*buttons)
    return markup
