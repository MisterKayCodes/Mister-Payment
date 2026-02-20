import os
import uuid
import aiofiles
from core.config import config

def generate_unique_filename(original_filename: str) -> str:
    """
    Generate a unique filename to prevent collisions.
    """
    ext = os.path.splitext(original_filename)[1]
    # If no extension is found, default to .jpg since it's a screenshot
    if not ext:
        ext = ".jpg"
    unique_name = f"{uuid.uuid4().hex}{ext}"
    return unique_name

async def save_screenshot(file_bytes: bytes, original_filename: str) -> str:
    """
    Save screenshot to storage/screenshots/ asynchronously and return full path.
    """
    # Directory check (already handled in config, but safe to keep)
    os.makedirs(config.SCREENSHOT_DIR, exist_ok=True)
    
    unique_name = generate_unique_filename(original_filename)
    file_path = os.path.join(config.SCREENSHOT_DIR, unique_name)
    
    # Using aiofiles to save without blocking the bot
    async with aiofiles.open(file_path, mode="wb") as f:
        await f.write(file_bytes)
        
    return file_path