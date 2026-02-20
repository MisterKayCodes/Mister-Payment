import os
import uuid
from core.config import config

def generate_unique_filename(original_filename: str) -> str:
    """
    Generate a unique filename to prevent collisions.
    """
    ext = os.path.splitext(original_filename)[1]
    unique_name = f"{uuid.uuid4().hex}{ext}"
    return unique_name

def save_screenshot(file_bytes: bytes, original_filename: str) -> str:
    """
    Save screenshot to storage/screenshots/ and return full path.
    """
    os.makedirs(config.SCREENSHOT_DIR, exist_ok=True)
    unique_name = generate_unique_filename(original_filename)
    file_path = os.path.join(config.SCREENSHOT_DIR, unique_name)
    with open(file_path, "wb") as f:
        f.write(file_bytes)
    return file_path