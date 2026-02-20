from functools import wraps
from aiogram import types
from core.config import config

def is_admin(user_id: int) -> bool:
    """
    Check if a user ID belongs to the admin.
    """
    return user_id == config.ADMIN_USER_ID

def require_admin(func):
    """
    Decorator to protect handlers for admin-only access.
    """
    @wraps(func)
    async def wrapper(message: types.Message, *args, **kwargs):
        if not is_admin(message.from_user.id):
            await message.reply("❌ You are not authorized to use this command.")
            return
        return await func(message, *args, **kwargs)
    return wrapper