import asyncio
import logging
import sys
from aiogram import Bot, Dispatcher, types, F
from aiogram.fsm.storage.memory import MemoryStorage

# Імпорт наших роутерів
from handlers.navigation import nav_router
from handlers.search_logic import search_router
from handlers.export import export_router
from handlers.results import results_router
from keyboards import get_main_menu

# КОНФІГУРАЦІЯ (Твій валідний токен)
TOKEN = "8780973686:AAEj3ioxDd-nRfJonyAGl37ufVtvq1kdi4M"

async def main():
    # Налаштування логування
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[logging.StreamHandler(sys.stdout)]
    )

    # Ініціалізація бота з перевіркою токена
    bot = Bot(token=TOKEN)
    dp = Dispatcher(storage=MemoryStorage())

    # Реєстрація роутерів
    dp.include_router(nav_router)
    dp.include_router(search_router)
    dp.include_router(export_router)
    dp.include_router(results_router)

    # Хендлер для команди /start (винесено в окрему функцію для надійності)
    @dp.message(F.text == "/start")
    async def cmd_start(message: types.Message):
        await message.answer(
            "⚡️ **EXARA OSINT TERMINAL**\nСистема активована. Оберіть дію:",
            reply_markup=get_main_menu(),
            parse_mode="Markdown"
        )

    print("[!] EXARA Client Bot запущений успішно...")
    
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print("[!] Бот зупинений.")
