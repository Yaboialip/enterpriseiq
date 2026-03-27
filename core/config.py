import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
DB_PATH = os.getenv("DB_PATH", "data/database.db")
MODEL_NAME = "gemini-2.5-flash"
APP_NAME = "EnterpriseIQ"