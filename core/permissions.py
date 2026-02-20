from aiogram import types
from aiogram.filters import BaseFilter
from core.config import config

class AdminFilter(BaseFilter):
    """
    A filter to check if the user is the admin.
    Usage: @router.message(AdminFilter())
    """
    async def __call__(self, message: types.Message) -> bool:
        is_admin = message.from_user.id == config.ADMIN_USER_ID
        
        if not is_admin:
            # Optional: Notify user they aren't authorized
            # Note: Filters usually just return False to let other handlers try,
            # but if you want to explicitly block and reply, you can do it here:
            await message.reply("❌ You are not authorized to use this command.")
            
        return is_admin

def is_admin(user_id: int) -> bool:
    """
    Simple helper for non-handler logic.
    """
    return user_id == config.ADMIN_USER_ID