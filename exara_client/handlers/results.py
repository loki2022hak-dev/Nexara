import aiopg
import json
from aiogram import Router, types, F
from aiogram.utils.keyboard import InlineKeyboardBuilder

results_router = Router()
DSN = "dbname=exara_db user=admin password=your_password host=127.0.0.1"

@results_router.message(F.text == "📊 Мої результати")
async def list_recent_scans(message: types.Message):
    async with aiopg.create_pool(DSN) as pool:
        async with pool.cursor() as cur:
            # Отримуємо останні 5 запитів користувача
            await cur.execute(
                "SELECT target_id, query, status, created_at FROM scan_targets "
                "WHERE user_id = %s ORDER BY created_at DESC LIMIT 5",
                (message.from_user.id,)
            )
            rows = await cur.fetchall()
            
            if not rows:
                await message.answer("📭 Ви ще не проводили пошуків.")
                return

            kb = InlineKeyboardBuilder()
            text = "📂 **ВАШІ ОСТАННІ ПОШУКИ:**\n\n"
            
            for row in rows:
                target_id, query, status, date = row
                status_emoji = "✅" if status == 'completed' else "⏳"
                text += f"{status_emoji} `{query}` — {date.strftime('%d.%m %H:%M')}\n"
                kb.row(types.InlineKeyboardButton(
                    text=f"👁 Переглянути {query}", 
                    callback_data=f"view_{target_id}"
                ))
            
            await message.answer(text, reply_markup=kb.as_markup(), parse_mode="Markdown")

@results_router.callback_query(F.data.startswith("view_"))
async def view_target_details(callback: types.CallbackQuery):
    target_id = callback.data.split("_")[1]
    
    async with aiopg.create_pool(DSN) as pool:
        async with pool.cursor() as cur:
            await cur.execute(
                "SELECT module_name, raw_data FROM scan_results WHERE target_id = %s",
                (target_id,)
            )
            results = await cur.fetchall()
            
            if not results:
                await callback.answer("Результатів поки немає або пошук триває.", show_alert=True)
                return

            report = "📋 **ДЕТАЛЬНИЙ ЗВІТ:**\n\n"
            for module, data in results:
                res_json = data # data вже є dict через JSONB
                report += f"🔹 **{res_json.get('site', 'Unknown')}**: {res_json.get('url', 'N/A')}\n"
            
            # Якщо звіт задовгий, Telegram може видати помилку, тому розбиваємо або обмежуємо
            await callback.message.answer(report, parse_mode="Markdown", disable_web_page_preview=True)
            await callback.answer()
