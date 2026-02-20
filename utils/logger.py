import logging
import os
from core.config import config

def setup_logger(log_dir: str = None):
    """
    Configure central logger for bot.
    """
    log_dir = log_dir or config.LOG_DIR
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, "mister_payment.log")

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.FileHandler(log_file, encoding="utf-8"),
            logging.StreamHandler()
        ]
    )

logger = logging.getLogger("mister_payment")