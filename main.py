import asyncio
import logging
import sys
from aiogram import Bot, Dispatcher
from app.config import settings
from app.db import init_db
from app.handlers import common, search, billing

# 1. Налаштування логів
logging.basicConfig(level=logging.INFO, stream=sys.stdout)

async def main():
    # 2. Ініціалізація бази та патч схеми (fix request_count)
    init_db()
    
    # 3. Ініціалізація бота
    bot = Bot(token=settings.BOT_TOKEN)
    dp = Dispatcher()
    
    # 4. Реєстрація роутерів (підключення меню та логіки)
    # Ми підключаємо їх у черговості пріоритету
    dp.include_router(common.router)   # Головне меню
    dp.include_router(search.router)   # Пошук
    dp.include_router(billing.router)  # Оплата/VIP

    print("🚀 GUARDIAN OSINT: Entrypoint підключено. Система в онлайні.")
    
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run(main())
