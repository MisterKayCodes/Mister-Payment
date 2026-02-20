from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from core.enums import CallbackActions, PaymentReviewCallback 

def generate_admin_keyboard(request_id: str) -> InlineKeyboardMarkup:
    """
    Generate approve/decline inline buttons for admin using the 3.x Builder.
    """
    builder = InlineKeyboardBuilder()

    builder.button(
        text="✅ Approve",
        callback_data=PaymentReviewCallback(action=CallbackActions.APPROVE, request_id=request_id)
    )
    builder.button(
        text="❌ Decline",
        callback_data=PaymentReviewCallback(action=CallbackActions.DECLINE, request_id=request_id)
    )

    builder.adjust(2)
    return builder.as_markup()