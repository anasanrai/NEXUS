import os
from dotenv import load_dotenv

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "")
MODEL_PRIMARY = os.getenv("PRIMARY_BRAIN_MODEL", "minimax/minimax-m2.5")
MODEL_BROWSER = os.getenv("BROWSER_RESEARCH_MODEL", "z-ai/glm-5")
MODEL_FAST = os.getenv("FAST_LOOPS_MODEL", "google/gemini-2.0-flash")
MODEL_FALLBACK = os.getenv("FALLBACK_PRECISION_MODEL", "anthropic/claude-3-5-sonnet")

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

REDIS_URL = os.getenv("REDIS_URL")

N8N_URL = os.getenv("N8N_URL")
N8N_API_KEY = os.getenv("N8N_API_KEY")

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
VERCEL_TOKEN = os.getenv("VERCEL_TOKEN")

SMTP_HOST = os.getenv("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASSWORD = os.getenv("SMTP_PASS")
