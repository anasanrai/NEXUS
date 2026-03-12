"""
NEXUS Configuration Module
Loads and manages all environment variables and global settings.
"""

import os
from typing import Optional
from dataclasses import dataclass
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


@dataclass
class LLMConfig:
    """Language Model configuration."""
    openrouter_api_key: str = os.getenv("OPENROUTER_API_KEY", "")
    gemini_api_key: str = os.getenv("GEMINI_API_KEY", "")
    anthropic_api_key: str = os.getenv("ANTHROPIC_API_KEY", "")
    
    primary_model: str = "minimax/minimax-m2.5"
    browser_model: str = "z-ai/glm-5"
    fast_model: str = "google/gemini-2.5-flash"
    fallback_model: str = "anthropic/claude-sonnet-4-5"


@dataclass
class TelegramConfig:
    """Telegram bot configuration."""
    bot_token: str = os.getenv("TELEGRAM_BOT_TOKEN", "")
    chat_id: str = os.getenv("TELEGRAM_CHAT_ID", "")


@dataclass
class DatabaseConfig:
    """Database configuration."""
    supabase_url: str = os.getenv("SUPABASE_URL", "")
    supabase_key: str = os.getenv("SUPABASE_KEY", "")
    redis_url: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")


@dataclass
class SearchConfig:
    """Search configuration."""
    tavily_api_key: str = os.getenv("TAVILY_API_KEY", "")


@dataclass
class GitConfig:
    """Git/GitHub configuration."""
    github_token: str = os.getenv("GITHUB_TOKEN", "")


@dataclass
class DeploymentConfig:
    """Deployment configuration."""
    vercel_token: str = os.getenv("VERCEL_TOKEN", "")
    vercel_project_id: str = os.getenv("VERCEL_PROJECT_ID", "")


@dataclass
class WorkflowConfig:
    """n8n workflow configuration."""
    n8n_url: str = os.getenv("N8N_URL", "http://localhost:5678")
    n8n_api_key: str = os.getenv("N8N_API_KEY", "")


@dataclass
class WordPressConfig:
    """WordPress configuration."""
    wordpress_url: str = os.getenv("WORDPRESS_URL", "")
    wordpress_user: str = os.getenv("WORDPRESS_USER", "")
    wordpress_password: str = os.getenv("WORDPRESS_PASSWORD", "")


@dataclass
class MediaConfig:
    """Media generation configuration."""
    deepgram_api_key: str = os.getenv("DEEPGRAM_API_KEY", "")
    fish_audio_key: str = os.getenv("FISH_AUDIO_KEY", "")
    replicate_api_token: str = os.getenv("REPLICATE_API_TOKEN", "")


@dataclass
class PaymentConfig:
    """Payment configuration."""
    stripe_key: str = os.getenv("STRIPE_KEY", "")


@dataclass
class SocialConfig:
    """Social media configuration."""
    twitter_api_key: str = os.getenv("TWITTER_API_KEY", "")
    twitter_api_secret: str = os.getenv("TWITTER_API_SECRET", "")
    twitter_access_token: str = os.getenv("TWITTER_ACCESS_TOKEN", "")
    twitter_access_secret: str = os.getenv("TWITTER_ACCESS_SECRET", "")
    linkedin_access_token: str = os.getenv("LINKEDIN_ACCESS_TOKEN", "")
    instagram_access_token: str = os.getenv("INSTAGRAM_ACCESS_TOKEN", "")


@dataclass
class EmailConfig:
    """Email configuration."""
    smtp_server: str = os.getenv("SMTP_SERVER", "smtp.gmail.com")
    smtp_port: int = int(os.getenv("SMTP_PORT", "587"))
    smtp_email: str = os.getenv("SMTP_EMAIL", "")
    smtp_password: str = os.getenv("SMTP_PASSWORD", "")


@dataclass
class AppConfig:
    """Application configuration."""
    environment: str = os.getenv("ENVIRONMENT", "development")
    log_level: str = os.getenv("LOG_LEVEL", "INFO")
    debug: bool = os.getenv("DEBUG", "False").lower() == "true"
    agent_timeout: int = int(os.getenv("AGENT_TIMEOUT", "300"))


@dataclass
class NEXUSConfig:
    """Main NEXUS configuration combining all sub-configurations."""
    llm: LLMConfig
    telegram: TelegramConfig
    database: DatabaseConfig
    search: SearchConfig
    git: GitConfig
    deployment: DeploymentConfig
    workflow: WorkflowConfig
    wordpress: WordPressConfig
    media: MediaConfig
    payment: PaymentConfig
    social: SocialConfig
    email: EmailConfig
    app: AppConfig


def load_config() -> NEXUSConfig:
    """
    Load all configuration from environment variables.
    
    Returns:
        NEXUSConfig: Complete configuration object
    """
    return NEXUSConfig(
        llm=LLMConfig(),
        telegram=TelegramConfig(),
        database=DatabaseConfig(),
        search=SearchConfig(),
        git=GitConfig(),
        deployment=DeploymentConfig(),
        workflow=WorkflowConfig(),
        wordpress=WordPressConfig(),
        media=MediaConfig(),
        payment=PaymentConfig(),
        social=SocialConfig(),
        email=EmailConfig(),
        app=AppConfig(),
    )


def validate_config(config: NEXUSConfig) -> bool:
    """
    Validate that all required configuration values are present.
    
    Args:
        config: Configuration object to validate
        
    Returns:
        bool: True if all required configs are present
    """
    required_fields = [
        config.llm.openrouter_api_key,
        config.telegram.bot_token,
        config.database.supabase_url,
        config.database.supabase_key,
        config.search.tavily_api_key,
        config.git.github_token,
    ]
    
    return all(required_fields)


# Global configuration instance
config = load_config()
