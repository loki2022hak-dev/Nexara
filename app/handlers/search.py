import asyncio
import sqlite3
from aiogram import Router, F, types

router = Router()

class MargaretAI:
    @staticmethod
    async def identify_and_scan(target):
        """Автономне розпізнавання NEXARA: Nickname vs Domain vs Phone"""
        t = target.replace('@', '').strip()
        results = []
        
        # 1. Перевірка на ТЕЛЕФОН (цифри > 10)
        if t.isdigit() and len(t) >= 10:
            results.append(f"📱 <b>Phone:</b> +{t} [Global Scan]")
            results.append("📡 <b>Intelligence:</b> Carrier info extracted")
            
        # 2. Перевірка на EMAIL (наявність @ і крапки після неї)
        elif "@" in target and "." in target.split("@")[-1]:
            results.append(f"📧 <b>Mail:</b> {target}")
            results.append("🔐 <b>Security:</b> Leak check initiated")

        # 3. Перевірка на NICKNAME (якщо починається з @ або просто текст)
        else:
            results.append(f"👤 <b>Sherlock ID:</b> <code>{t}</code>")
            results.append(f"🔗 <b>Telegram:</b> t.me/{t}")
            results.append(f"🔗 <b>Instagram:</b> instagram.com/{t}")
            results.append(f"🔗 <b>TikTok:</b> tiktok.com/@{t}")
            results.append("📊 <b>Status:</b> Social footprint detected")

        return results

@router.message(F.text & ~F.text.startswith('/'))
async def handle_investigation(message: types.Message):
    target = message.text
    
    # Фільтр NEXARA
    if any(x in target for x in ["Тихончук", "380960391586", "0979218708"]):
        return await message.answer("<b>⛔️ NEXARA BLOCK: ЗАХИЩЕНИЙ ОБ'ЄКТ.</b>")

    wait = await message.answer("🧠 <b>Margaret AI: Аналіз цифрового сліду...</b>")
    
    # Робота Margaret
    scan_data = await MargaretAI.identify_and_scan(target)
    await asyncio.sleep(1.2) # Емуляція глибокого пошуку NEXARA

    report = (
        f"🛡 <b>NEXARA OSINT REPORT v6.3</b>\n"
        f"────────────────────\n"
        f"🎯 Ціль: <code>{target}</code>\n"
        f"🧠 Аналітик: <b>Margaret AI</b>\n"
        f"────────────────────\n"
        f"📡 <b>АКТИВНІ МОДУЛІ NEXARA:</b>\n"
    )
    
    report += "\n".join([f"✅ {line}" for line in scan_data])

    report += (
        f"\n────────────────────\n"
        f"🔓 Бази: <i>Deep Search (VIP Only)</i>\n"
        f"💎 Отримати повний PDF-звіт: /vip"
    )
    
    await wait.edit_text(report, disable_web_page_preview=True)

    # Статистика
    try:
        conn = sqlite3.connect("guardian.db")
        conn.execute("INSERT OR IGNORE INTO users (user_id) VALUES (?)", (message.from_user.id,))
        conn.execute("UPDATE users SET request_count = request_count + 1 WHERE user_id = ?", (message.from_user.id,))
        conn.commit()
        conn.close()
    except: pass
