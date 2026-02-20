from aiogram import types, Router
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup
from bot.keyboards.payment_methods import generate_payment_keyboard
from services.payment_service import get_active_currencies

# In v3, we use Routers to organize handlers
router = Router()

@router.message(Command("start"))
async def start_command(message: types.Message):
    """
    /start command — show user active currencies.
    """
    currencies = get_active_currencies()
    
    if not currencies:
        await message.answer("No payment methods available. Please try later.")
        return
    
    # Ensure your generate_payment_keyboard function returns 
    # an InlineKeyboardMarkup object compatible with v3
    keyboard = generate_payment_keyboard(currencies)
    
    await message.answer(
        "💰 Please select your payment currency:", 
        reply_markup=keyboard
    )