import os
from dotenv import load_dotenv
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:pass@localhost:5432/wqdb")
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "openai")  # 'openai' or 'gemini'
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
MAX_QUESTIONS = int(os.getenv("MAX_QUESTIONS", "7"))
