from aiogram import types
from services.payment_service import create_payment_request
from utils.file_manager import save_screenshot
from utils.logger import logger
from core.config import config

async def handle_screenshot(message: types.Message):
    """
    Handles user sending screenshot of payment.
    """
    if not message.photo:
        await message.reply("Please send a valid image file.")
        return
    
    photo = message.photo[-1]
    file_bytes = await photo.download(destination=bytes)
    file_path = save_screenshot(file_bytes, f"{photo.file_id}.jpg")
    
    request = create_payment_request(
        user_id=message.from_user.id,
        username=message.from_user.username or message.from_user.full_name,
        currency="Unknown",  # Could be enhanced to track selected currency
        screenshot_path=file_path
    )
    
    # Notify admin
    admin_msg = (
        f"📩 New payment request:\n"
        f"User: @{request['username']}\n"
        f"Currency: {request['currency']}\n"
        f"Request ID: {request['id']}"
    )
    
    await message.bot.send_message(chat_id=config.ADMIN_USER_ID, text=admin_msg)
    
    await message.reply("✅ Screenshot received! Pending verification.")
    logger.info(f"User {message.from_user.id} uploaded screenshot: {file_path}")