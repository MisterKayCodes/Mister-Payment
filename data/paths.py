import os
from core.config import config

# Ensure storage directories exist
os.makedirs(config.STORAGE_DIR, exist_ok=True)
os.makedirs(config.SCREENSHOT_DIR, exist_ok=True)

# JSON storage paths
PAYMENT_METHODS_FILE = config.PAYMENT_METHODS_FILE
PAYMENT_REQUESTS_FILE = config.PAYMENT_REQUESTS_FILE
BOT_CONFIG_FILE = config.BOT_CONFIG_FILE
SCREENSHOT_DIR = config.SCREENSHOT_DIR