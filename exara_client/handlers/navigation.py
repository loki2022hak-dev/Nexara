from aiogram import F, Router, types
from keyboards import get_main_menu

nav_router = Router()

@nav_router.message(F.text == "👤 Профіль")
async def nav_profile(message: types.Message):
    await message.answer(f"👤 **ПРОФІЛЬ**\nID: `{message.from_user.id}`\nСтатус: VIP 💎", parse_mode="Markdown")

@nav_router.message(F.text == "⚙️ Налаштування")
async def nav_settings(message: types.Message):
    await message.answer("⚙️ **НАЛАШТУВАННЯ**\nТут можна змінити параметри пошуку.")

@nav_router.message(F.text == "❓ Допомога")
async def nav_help(message: types.Message):
    await message.answer("❓ **ДОПОМОГА**\nНапишіть @admin для підтримки.")
