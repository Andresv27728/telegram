"""
Configuration module for the Telegram bot.
Handles environment variables and bot settings.
"""
import os
from typing import Optional
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Configuration class for bot settings."""
    
    def __init__(self):
        # Try to load token from file first, then environment variable
        self.BOT_TOKEN: str = self._load_token_from_file() or os.getenv("BOT_TOKEN", "")
        self.LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
        self.WEBHOOK_URL: Optional[str] = os.getenv("WEBHOOK_URL")
        # Web server configuration - compatible with Render
        self.PORT: int = int(os.getenv("PORT", os.getenv("WEB_PORT", "5000")))
    
    def _load_token_from_file(self) -> str:
        """Load bot token from token.txt file if it exists."""
        try:
            if os.path.exists("token.txt"):
                with open("token.txt", "r", encoding="utf-8") as f:
                    token = f.read().strip()
                    if token:
                        return token
        except Exception:
            pass
        return ""
        
    def validate(self) -> bool:
        """Validate that required configuration is present."""
        if not self.BOT_TOKEN:
            return False
        return True
    
    def get_missing_vars(self) -> list:
        """Get list of missing required environment variables."""
        missing = []
        if not self.BOT_TOKEN:
            missing.append("BOT_TOKEN")
        return missing

# Global config instance
config = Config()
