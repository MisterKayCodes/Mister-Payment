from aiogram import types
from aiogram.types import InlineKeyboardMarkup
from bot.keyboards.payment_methods import generate_payment_keyboard
from services.payment_service import get_active_currencies

async def start_command(message: types.Message):
    """
    /start command — show user active currencies.
    """
    currencies = get_active_currencies()
    if not currencies:
        await message.answer("No payment methods available. Please try later.")
        return
    
    keyboard = generate_payment_keyboard(currencies)
    await message.answer("💰 Please select your payment currency:", reply_markup=keyboard)