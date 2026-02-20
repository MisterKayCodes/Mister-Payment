import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    # Bot token - Added a check to ensure the bot doesn't start without a token
    BOT_TOKEN: str = os.getenv("BOT_TOKEN", "")
    if not BOT_TOKEN:
        raise ValueError("❌ BOT_TOKEN is missing! Please check your .env file.")
    
    # Admin info - Converting to int safely
    try:
        ADMIN_USER_ID: int = int(os.getenv("ADMIN_USER_ID", 0))
    except (ValueError, TypeError):
        ADMIN_USER_ID = 0
    
    # Storage and logs
    STORAGE_DIR: str = os.getenv("STORAGE_DIR", "storage")
    LOG_DIR: str = os.getenv("LOG_DIR", "logs")
    
    # File upload limits
    MAX_FILE_SIZE_MB: int = int(os.getenv("MAX_FILE_SIZE_MB", 5))
    
    # JSON files - Using os.path.join for cross-platform compatibility
    # Ensure the storage directory exists so the bot doesn't crash on first run
    os.makedirs(STORAGE_DIR, exist_ok=True)
    
    PAYMENT_METHODS_FILE: str = os.path.join(STORAGE_DIR, "payment_methods.json")
    PAYMENT_REQUESTS_FILE: str = os.path.join(STORAGE_DIR, "payment_requests.json")
    BOT_CONFIG_FILE: str = os.path.join(STORAGE_DIR, "bot_config.json")
    
    SCREENSHOT_DIR: str = os.path.join(STORAGE_DIR, "screenshots")
    os.makedirs(SCREENSHOT_DIR, exist_ok=True) # Create screenshots folder automatically

# Single config instance for convenience
config = Config()