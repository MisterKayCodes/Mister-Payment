from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def generate_payment_keyboard(currencies):
    """
    Generate a dynamic inline keyboard with all available currencies.
    """
    keyboard = InlineKeyboardMarkup(row_width=1)  # 1 button per row
    for c in currencies:
        keyboard.add(InlineKeyboardButton(text=c, callback_data=f"pay_{c}"))
    return keyboard