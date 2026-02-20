import json
import os
from aiogram import types
from aiogram.filters import BaseFilter
from core.config import config

class AdminFilter(BaseFilter):
    async def __call__(self, message: types.Message) -> bool:
        user_id = message.from_user.id
        
        # 1. Always allow the Master Admin from .env
        if user_id == config.ADMIN_USER_ID:
            return True
            
        # 2. Check if this user has been "Crowned" in the config file
        if os.path.exists(config.BOT_CONFIG_FILE):
            try:
                with open(config.BOT_CONFIG_FILE, "r") as f:
                    data = json.load(f)
                    authorized_admins = data.get("authorized_admins", [])
                    # Convert to strings for safe comparison
                    if str(user_id) in [str(a) for a in authorized_admins]:
                        return True
            except Exception:
                pass

        return False

async def is_admin(user_id: int) -> bool:
    """
    Improved helper that checks both the .env and the JSON config.
    """
    if user_id == config.ADMIN_USER_ID:
        return True
        
    if os.path.exists(config.BOT_CONFIG_FILE):
        try:
            with open(config.BOT_CONFIG_FILE, "r") as f:
                data = json.load(f)
                authorized = data.get("authorized_admins", [])
                return str(user_id) in [str(a) for a in authorized]
        except:
            return False
    return False