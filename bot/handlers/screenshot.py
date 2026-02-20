import io
from aiogram import types, Router, F
from services.payment_service import create_payment_request
from utils.file_manager import save_screenshot
from utils.logger import logger
from core.config import config

router = Router()

@router.message(F.photo)
async def handle_screenshot(message: types.Message):
    """
    Handles user sending screenshot of payment.
    """
    # In v3, the F.photo filter ensures message.photo exists
    photo = message.photo[-1]
    
    # NEW v3 DOWNLOAD METHOD:
    # Use bot.download() instead of photo.download()
    file_info = await message.bot.get_file(photo.file_id)
    file_bytes = await message.bot.download_file(file_info.file_path)
    
    # Convert the BytesIO object to raw bytes for your save_screenshot function
    raw_bytes = file_bytes.read()
    
    file_path = save_screenshot(raw_bytes, f"{photo.file_id}.jpg")
    
    request = create_payment_request(
        user_id=message.from_user.id,
        username=message.from_user.username or message.from_user.full_name,
        currency="Unknown",
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