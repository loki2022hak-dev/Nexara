import json
import redis.asyncio as redis
from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

class SearchStates(StatesGroup):
    waiting_for_query = State()

search_router = Router()
r = redis.from_url("redis://localhost")

# Список системних назв кнопок, які НЕ є пошуковими запитами
MENU_BUTTONS = [
    "🔍 Новий пошук", "📊 Мої результати", "🛠 Інструменти",
    "💎 VIP / Тарифи", "👤 Профіль", "⚙️ Налаштування", "❓ Допомога", "⬅️ Назад"
]

@search_router.message(F.text == "🔍 Новий пошук")
async def start_search(message: types.Message, state: FSMContext):
    await state.set_state(SearchStates.waiting_for_query)
    await message.answer("🎯 **РЕЖИМ ПОШУКУ**\nВведіть Username для аналізу:")

@search_router.message(SearchStates.waiting_for_query)
async def process_search(message: types.Message, state: FSMContext):
    # Якщо користувач натиснув іншу кнопку меню замість вводу тексту
    if message.text in MENU_BUTTONS:
        await state.clear()
        # Дозволяємо іншим роутерам обробити цю кнопку
        return 

    query = message.text.strip()
    task_data = {
        "target_id": "550e8400-e29b-41d4-a716-446655440000",
        "query": query,
        "user_id": message.from_user.id
    }
    
    await r.lpush("exara_tasks_high", json.dumps(task_data))
    await message.answer(f"🚀 Запит `{query}` додано в чергу.")
    await state.clear()
