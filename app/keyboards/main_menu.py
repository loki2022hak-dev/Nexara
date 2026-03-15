from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def main_menu():
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="🔎 Нове розслідування"),
                KeyboardButton(text="📁 Мої звіти"),
            ],
            [
                KeyboardButton(text="🤖 Питання AI"),
                KeyboardButton(text="⚙️ Налаштування"),
            ]
        ],
        resize_keyboard=True
    )
