import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN", "8780973686:AAEj3ioxDd-nRfJonyAGl37ufVtvq1kdi4M")
DATABASE_URL = "sqlite:///./guardian.db" # Локальна база
