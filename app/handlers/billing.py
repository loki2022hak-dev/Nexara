from aiogram import Router, types, F
from aiogram.filters import Command
import sqlite3

router = Router()

@router.message(Command("vip"))
async def vip_menu(message: types.Message):
    # Отримуємо статус з бази
    conn = sqlite3.connect("guardian.db")
    user = conn.execute("SELECT is_vip, request_count FROM users WHERE user_id = ?", (message.from_user.id,)).fetchone()
    conn.close()
    
    status = "👑 VIP АКТИВНИЙ" if user and user[0] else "❌ ТАРИФ: FREE"
    requests = user[1] if user else 0

    text = (
        f"👤 **ПРОФІЛЬ КОРИСТУВАЧА**\n"
        f"────────────────────\n"
        f"🆔 ID: `{message.from_user.id}`\n"
        f"📊 Статус: `{status}`\n"
        f"🔍 Запитів зроблено: `{requests}`\n"
        f"────────────────────\n"
        f"💳 **ДОСТУПНІ ТАРИФИ:**\n"
        f"• **START:** 50 запитів — 10$\n"
        f"• **ULTRA (VIP):** Безліміт — 25$\n"
        f"────────────────────\n"
        f"💎 *VIP відкриває доступ до баз МВС, камер (Scanner) та Sherlock Pro.*"
    )
    
    kb = types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(text="💎 Купити VIP", url="https://t.me/admin_user")],
        [types.InlineKeyboardButton(text="🔄 Оновити статус", callback_data="refresh")]
    ])
    
    await message.answer(text, reply_markup=kb, parse_mode="Markdown")

@router.message(Command("price"))
async def price_cmd(message: types.Message):
    await vip_menu(message)
