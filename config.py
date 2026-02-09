import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

DB_URL = "sqlite:///dq_ai.db"

LEARNING_DAYS = 7
Z_THRESHOLD = 3