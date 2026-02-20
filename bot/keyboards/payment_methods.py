from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

def generate_payment_keyboard(methods: list) -> InlineKeyboardMarkup:
    """
    Creates a keyboard with one payment method per row.
    'methods' is now a list of dictionaries.
    """
    builder = InlineKeyboardBuilder()

    for m in methods:
        # m is a dictionary, so m['currency'] works!
        builder.row(InlineKeyboardButton(
            text=f"💰 {m['currency']} - {m['label']}", 
            callback_data=f"pay_{m['id']}"
        ))

    return builder.as_markup()