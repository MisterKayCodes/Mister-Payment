import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    # Bot token
    BOT_TOKEN: str = os.getenv("BOT_TOKEN", "")
    
    # Admin info
    ADMIN_USER_ID: int = int(os.getenv("ADMIN_USER_ID", 0))
    
    # Storage and logs
    STORAGE_DIR: str = os.getenv("STORAGE_DIR", "storage")
    LOG_DIR: str = os.getenv("LOG_DIR", "logs")
    
    # File upload limits
    MAX_FILE_SIZE_MB: int = int(os.getenv("MAX_FILE_SIZE_MB", 5))
    
    # JSON files
    PAYMENT_METHODS_FILE: str = os.path.join(STORAGE_DIR, "payment_methods.json")
    PAYMENT_REQUESTS_FILE: str = os.path.join(STORAGE_DIR, "payment_requests.json")
    BOT_CONFIG_FILE: str = os.path.join(STORAGE_DIR, "bot_config.json")
    SCREENSHOT_DIR: str = os.path.join(STORAGE_DIR, "screenshots")

# Single config instance for convenience
config = Config()