from aiogram import types, Router, F
from aiogram.filters import Command
from core.permissions import AdminFilter  # I recommend changing your decorator to a Filter
from services.admin_service import (
    add_payment_method, edit_payment_method, 
    delete_payment_method, list_payment_methods, set_admin_contact
)
from services.verification_service import get_pending_requests, update_payment_status
from bot.keyboards.admin_actions import generate_admin_keyboard

router = Router()

# You can apply the AdminFilter to the entire router 
# so you don't have to repeat it for every function!
router.message.filter(AdminFilter()) 

@router.message(Command("add_method"))
async def add_method_handler(message: types.Message):
    await message.reply("📝 Command to add payment method.\nFormat: `currency,label,name,address`", parse_mode="Markdown")

@router.message(Command("edit_method"))
async def edit_method_handler(message: types.Message):
    await message.reply("✏️ Command to edit payment method.\nFormat: `id,field,value`", parse_mode="Markdown")

@router.message(Command("delete_method"))
async def delete_method_handler(message: types.Message):
    await message.reply("🗑️ Command to delete payment method.\nFormat: `id`", parse_mode="Markdown")

@router.message(Command("list_methods"))
async def list_methods_handler(message: types.Message):
    methods = list_payment_methods()
    lines = [
        f"🆔 {m['id']}: {m['currency']} - {m['label']} ({'✅ Active' if m['is_active'] else '❌ Inactive'})" 
        for m in methods
    ]
    await message.reply("\n".join(lines) or "No payment methods found.")

@router.message(Command("set_contact"))
async def set_admin_contact_handler(message: types.Message):
    await message.reply("👤 Command to set new admin.\nFormat: `username,user_id`", parse_mode="Markdown")

@router.message(Command("pending"))
async def pending_payments_handler(message: types.Message):
    requests = get_pending_requests()
    
    if not requests:
        await message.answer("☕ No pending payments at the moment.")
        return

    for r in requests:
        text = (
            f"📩 **Request ID:** {r['id']}\n"
            f"👤 **User:** @{r['username']}\n"
            f"💰 **Currency:** {r['currency']}"
        )
        # Ensure your keyboard generator is updated for v3 (using InlineKeyboardBuilder)
        keyboard = generate_admin_keyboard(r['id'])
        await message.reply(text, reply_markup=keyboard, parse_mode="Markdown")