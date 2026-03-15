import json
import io
from aiogram import F, Router, types
from aiogram.fsm.context import FSMContext
from aiogram.types import BufferedInputFile
from states import ExportStates

export_router = Router()

@export_router.message(F.text == "📤 Експорт")
async def start_export(message: types.Message, state: FSMContext):
    await state.set_state(ExportStates.choosing_format)
    kb = types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(text="📄 PDF (Звіт)", callback_data="fmt_pdf")],
        [types.InlineKeyboardButton(text="💻 JSON (Сирі дані)", callback_data="fmt_json")],
        [types.InlineKeyboardButton(text="❌ Скасувати", callback_data="export_cancel")]
    ])
    await message.answer("🛠 **ГЕНЕРАЦІЯ ЗВІТУ**\nОберіть формат вивантаження даних:", reply_markup=kb)

@export_router.callback_query(F.data.startswith("fmt_"))
async def process_export(callback: types.CallbackQuery, state: FSMContext):
    fmt = callback.data.split("_")[1]
    await callback.message.edit_text(f"⏳ Формування {fmt.upper()}... Зачекайте.")
    
    # Симуляція отримання даних з твоїх 500+ модулів
    mock_data = {
        "report_id": "EX-9921",
        "target": "@target_user",
        "status": "COMPLETED",
        "modules_scanned": 512,
        "threat_level": "CRITICAL"
    }

    if fmt == "json":
        file_content = json.dumps(mock_data, indent=4).encode('utf-8')
        file = BufferedInputFile(file_content, filename="exara_report.json")
    else:
        # Для PDF тут буде виклик генератора (наприклад, reportlab)
        # Поки відправляємо як текстовий файл для тесту логіки
        file_content = f"EXARA REPORT\nID: {mock_data['report_id']}\nResult: SUCCESS".encode('utf-8')
        file = BufferedInputFile(file_content, filename="exara_report.pdf")

    await callback.message.answer_document(file, caption=f"✅ Звіт EXARA у форматі {fmt.upper()} готовий.")
    await state.clear()
    await callback.answer()

@export_router.callback_query(F.data == "export_cancel")
async def cancel_export(callback: types.CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.edit_text("❌ Експорт скасовано.")
    await callback.answer()
