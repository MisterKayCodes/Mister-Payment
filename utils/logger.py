import logging
import os
import sys
from core.config import config

def setup_logger(log_dir: str = None):
    """
    Configure central logger for bot with UTF-8 support for emojis.
    """
    log_dir = log_dir or config.LOG_DIR
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, "mister_payment.log")

    # Set up basic configuration
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        handlers=[
            # Encoding is important for those 💰 and ✅ emojis!
            logging.FileHandler(log_file, encoding="utf-8"),
            logging.StreamHandler(sys.stdout)
        ]
    )

# Create the logger instance
logger = logging.getLogger("mister_payment")

# Trigger the setup automatically so you don't have to call it everywhere
setup_logger()