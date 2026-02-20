from aiogram import types, Router
from aiogram.filters import Command

router = Router()

@router.message(Command("help"))
async def help_command(message: types.Message):
    help_text = (
        "<b>👋 Welcome to Mister Payment Help</b>\n\n"
        "<b>How to use this bot:</b>\n"
        "1️⃣ Use /start to see available currencies.\n"
        "2️⃣ Select your preferred payment method.\n"
        "3️⃣ Copy the address and make the payment.\n"
        "4️⃣ Upload a screenshot of your receipt here.\n\n"
        "<b>Admin Support:</b>\n"
        "If you have issues, contact our support team."
    )
    await message.answer(help_text)