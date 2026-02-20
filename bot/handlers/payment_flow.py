from aiogram import types, Router, F
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from services.payment_service import list_active_payment_methods

router = Router()

@router.message(F.text)
async def currency_selection(message: types.Message):
    """
    Shows payment method details for selected currency in aiogram v3.
    """
    # In v3, F.text ensures message.text is not None
    currency = message.text.strip().upper()
    methods = list_active_payment_methods()
    
    filtered = [m for m in methods if m["currency"] == currency]
    
    if not filtered:
        await message.answer("❌ No active payment methods for this currency.")
        return
    
    text_lines = []
    for m in filtered:
        text_lines.append(
            f"💳 {m['label']}\n"
            f"Name: {m['account_name']}\n"
            f"Account: {m['account_address']}"
        )
    
    reply_text = "\n\n".join(text_lines)
    
    await message.answer(
        f"{reply_text}\n\nAfter payment, please send your screenshot."
    )