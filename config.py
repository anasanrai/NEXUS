import os
from pathlib import Path
from dotenv import load_dotenv
from pydantic_settings import BaseSettings
from typing import Optional

# Load environment variables from .env file
load_dotenv()

class Settings(BaseSettings):
    # Base Directory
    BASE_DIR: Path = Path(__file__).resolve().parent

    # Core AI Configuration
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    OPENROUTER_API_KEY: str = os.getenv("OPENROUTER_API_KEY", "")
    DEFAULT_MODEL: str = os.getenv("DEFAULT_MODEL", "minimax/minimax-m2.5")
    EMBEDDING_MODEL: str = os.getenv("EMBEDDING_MODEL", "text-embedding-3-small")

    # Tiered Model Stack
    PRIMARY_BRAIN_MODEL: str = os.getenv("PRIMARY_BRAIN_MODEL", "minimax/minimax-m2.5")
    BROWSER_RESEARCH_MODEL: str = os.getenv("BROWSER_RESEARCH_MODEL", "z-ai/glm-5")
    FAST_LOOPS_MODEL: str = os.getenv("FAST_LOOPS_MODEL", "google/gemini-2.0-flash")
    FALLBACK_PRECISION_MODEL: str = os.getenv("FALLBACK_PRECISION_MODEL", "anthropic/claude-3-5-sonnet")

    # System Configuration
    DEBUG: bool = os.getenv("DEBUG", "True").lower() == "true"
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    APP_SECRET_KEY: str = os.getenv("APP_SECRET_KEY", "nexus-super-secret-key")

    # Channel Configuration
    TELEGRAM_BOT_TOKEN: Optional[str] = os.getenv("TELEGRAM_BOT_TOKEN")
    TELEGRAM_CHAT_ID: Optional[str] = os.getenv("TELEGRAM_CHAT_ID")

    # Tool Specific Keys
    SERPAPI_API_KEY: Optional[str] = os.getenv("SERPAPI_API_KEY")
    BROWSERLESS_API_KEY: Optional[str] = os.getenv("BROWSERLESS_API_KEY")
    VERCEL_TOKEN: Optional[str] = os.getenv("VERCEL_TOKEN")
    GITHUB_TOKEN: Optional[str] = os.getenv("GITHUB_TOKEN")
    N8N_API_KEY: Optional[str] = os.getenv("N8N_API_KEY")

    # Database / Memory
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./nexus.db")
    REDIS_URL: Optional[str] = os.getenv("REDIS_URL")

    # Email Configuration
    SMTP_HOST: str = os.getenv("SMTP_HOST", "smtp.gmail.com")
    SMTP_PORT: int = int(os.getenv("SMTP_PORT", "587"))
    SMTP_USER: Optional[str] = os.getenv("SMTP_USER")
    SMTP_PASS: Optional[str] = os.getenv("SMTP_PASS")

    class Config:
        env_file = ".env"
        case_sensitive = True

# Global settings instance
settings = Settings()
