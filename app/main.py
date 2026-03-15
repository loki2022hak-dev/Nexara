import asyncio
import logging
import sys
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

TOKEN = "8780973686:AAEj3ioxDd-nRfJonyAGl37ufVtvq1kdi4M"

from app.handlers import common, search, billing

async def main():
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher()

    dp.include_router(common.router)
    dp.include_router(search.router)
    dp.include_router(billing.router)

    print("🚀 NEXARA OSINT ENTERPRISE ЗАПУЩЕНО!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
