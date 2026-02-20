from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from core.enums import CallbackActions

def generate_admin_keyboard(request_id: str):
    """
    Generate approve/decline inline buttons for admin.
    """
    keyboard = InlineKeyboardMarkup(row_width=2)  # 2 buttons in one row
    approve_button = InlineKeyboardButton(
        text="✅ Approve",
        callback_data=f"{CallbackActions.APPROVE}_{request_id}"
    )
    decline_button = InlineKeyboardButton(
        text="❌ Decline",
        callback_data=f"{CallbackActions.DECLINE}_{request_id}"
    )
    keyboard.row(approve_button, decline_button)  # place both buttons in a single row
    return keyboard