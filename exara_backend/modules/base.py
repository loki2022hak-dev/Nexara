import asyncio
import json
import os

class OsintModule:
    def __init__(self, target):
        self.target = target

    async def run_sherlock(self):
        output_file = f"{self.target}_results.json"
        # --timeout 1 - ключовий параметр для швидкості
        # --no-color прибирає зайве навантаження на логування
        process = await asyncio.create_subprocess_exec(
            'python3', '-m', 'sherlock', self.target, 
            '--timeout', '1', 
            '--json', output_file,
            '--no-color',
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        
        print(f"[*] Sherlock стартував для: {self.target}")
        stdout, stderr = await process.communicate()
        
        results = []
        if os.path.exists(output_file):
            try:
                with open(output_file, 'r') as f:
                    data = json.load(f)
                    for site, info in data.items():
                        if info.get("status") == "claimed":
                            results.append({"site": site, "url": info.get("url_user")})
                os.remove(output_file)
            except Exception as e:
                print(f"[!] Помилка парсингу {self.target}: {e}")
        
        return results
