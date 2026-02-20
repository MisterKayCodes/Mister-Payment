from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def generate_payment_keyboard(currencies):
    keyboard = InlineKeyboardMarkup()
    for c in currencies:
        keyboard.add(InlineKeyboardButton(text=c, callback_data=f"pay_{c}"))
    return keyboard