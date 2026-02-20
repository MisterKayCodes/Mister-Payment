from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from core.enums import CallbackActions

def generate_admin_keyboard(request_id: str):
    keyboard = InlineKeyboardMarkup()
    keyboard.add(
        InlineKeyboardButton(text="✅ Approve", callback_data=f"{CallbackActions.APPROVE}_{request_id}"),
        InlineKeyboardButton(text="❌ Decline", callback_data=f"{CallbackActions.DECLINE}_{request_id}")
    )
    return keyboard