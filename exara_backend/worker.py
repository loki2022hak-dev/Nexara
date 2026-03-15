import asyncio
import json
import redis.asyncio as redis
import os
import aiohttp
from aiogram import Bot

# КОНФІГУРАЦІЯ
BOT_TOKEN = "8780973686:AAEj3ioxDd-nRfJonyAGl37ufVtvq1kdi4M"
VENICE_API_KEY = "VENICE_INFERENCE_KEY_tnDQI119jG8ehy7yBKw0If0sAkxufLoz1KQYySLMgj"

async def get_ai_analysis(query, found_sites):
    """Запит до Venice.ai для аналізу знайдених даних"""
    url = "https://api.venice.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {VENICE_API_KEY}",
        "Content-Type": "application/json"
    }
    
    sites_list = ", ".join(found_sites) if found_sites else "жодного сайту не знайдено"
    prompt = f"Зроби короткий OSINT-аналіз користувача з нікнеймом '{query}'. Він знайдений на таких ресурсах: {sites_list}. Що це може сказати про його інтереси чи діяльність? Відповідь дай українською мовою, лаконічно."

    payload = {
        "model": "llama-3.1-70b", # Або інша доступна модель Venice
        "messages": [{"role": "user", "content": prompt}]
    }

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, json=payload, timeout=15) as resp:
                result = await resp.json()
                return result['choices'][0]['message']['content']
    except Exception as e:
        return f"Аналіз ШІ тимчасово недоступний. ({e})"

async def process_task(task_data):
    data = json.loads(task_data)
    query = data['query']
    user_id = data['user_id']
    bot = Bot(token=BOT_TOKEN)

    print(f"[*] СТАРТ OSINT + AI: {query}")
    
    # 1. Запуск Sherlock
    process = await asyncio.create_subprocess_exec(
        'python3', '-m', 'sherlock', query, '--timeout', '1', '--json', f"{query}.json",
        stdout=asyncio.subprocess.DEVNULL, stderr=asyncio.subprocess.DEVNULL
    )
    await process.wait()
    
    # 2. Обробка результатів Sherlock
    found_sites = []
    if os.path.exists(f"{query}.json"):
        try:
            with open(f"{query}.json", 'r') as f:
                res = json.load(f)
                found_sites = [s for s in res if res[s]['status'] == 'claimed']
            os.remove(f"{query}.json")
        except: pass

    # 3. Аналіз через Venice AI
    ai_summary = await get_ai_analysis(query, found_sites)

    # 4. Формування звіту
    report = (
        f"✅ **ЗВІТ ЗАВЕРШЕНО ДЛЯ: `{query}`**\n\n"
        f"🔗 **Знайдено акаунтів:** `{len(found_sites)}`\n"
        f"🌐 **Ресурси:** {', '.join(found_sites[:10])}{'...' if len(found_sites) > 10 else ''}\n\n"
        f"🤖 **ШІ-АНАЛІЗ (Venice):**\n{ai_summary}"
    )

    try:
        await bot.send_message(user_id, report, parse_mode="Markdown")
    finally:
        await bot.session.close()

async def main():
    r = redis.from_url("redis://localhost")
    print("[!!!] EXARA 100% ENGINE + VENICE AI СТАРТУВАВ")
    while True:
        task = await r.brpop("exara_tasks_high", timeout=0)
        if task:
            asyncio.create_task(process_task(task[1].decode()))

if __name__ == "__main__":
    asyncio.run(main())
