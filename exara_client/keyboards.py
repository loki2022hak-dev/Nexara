from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram import types

def get_main_menu():
    kb = ReplyKeyboardBuilder()
    kb.row(types.KeyboardButton(text="🔍 Новий пошук"))
    kb.row(types.KeyboardButton(text="📊 Мої результати"), types.KeyboardButton(text="🛠 Інструменти"))
    kb.row(types.KeyboardButton(text="💎 VIP / Тарифи"), types.KeyboardButton(text="👤 Профіль"))
    kb.row(types.KeyboardButton(text="⚙️ Налаштування"), types.KeyboardButton(text="❓ Допомога"))
    return kb.as_markup(resize_keyboard=True)

def get_search_menu():
    kb = ReplyKeyboardBuilder()
    kb.row(types.KeyboardButton(text="👤 Username"), types.KeyboardButton(text="🔗 Посилання"))
    kb.row(types.KeyboardButton(text="⚡️ Швидка перевірка"), types.KeyboardButton(text="🔍 Розширена перевірка"))
    kb.row(types.KeyboardButton(text="📜 Історія цілей"), types.KeyboardButton(text="⬅️ Назад"))
    return kb.as_markup(resize_keyboard=True)

def get_results_menu():
    kb = ReplyKeyboardBuilder()
    kb.row(types.KeyboardButton(text="📄 Останній результат"))
    kb.row(types.KeyboardButton(text="📅 Історія"), types.KeyboardButton(text="💾 Збережені"))
    kb.row(types.KeyboardButton(text="📤 Експорт"), types.KeyboardButton(text="⬅️ Назад"))
    return kb.as_markup(resize_keyboard=True)
