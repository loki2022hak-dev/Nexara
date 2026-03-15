from aiogram import Router, types
from aiogram.filters import Command

router = Router()

@router.message(Command("start"))
async def start(message: types.Message):
    await message.answer(
        "🚀 <b>СИСТЕМА GUARDIAN АКТИВОВАНА</b>\n\n"
        "Введіть Email, IP або Username для пошуку.",
        parse_mode="HTML"
    )

@router.message(Command("help"))
async def help_cmd(message: types.Message):
    await message.answer(
        "🛠 <b>ДОСТУПНІ КОМАНДИ:</b>\n"
        "/start - Запуск\n"
        "/vip - VIP статус\n"
        "/price - Ціни",
        parse_mode="HTML"
    )
