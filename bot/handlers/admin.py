from aiogram import types
from core.permissions import require_admin
from services.admin_service import add_payment_method, edit_payment_method, delete_payment_method, list_payment_methods, set_admin_contact
from services.verification_service import get_pending_requests, update_payment_status
from bot.keyboards.admin_actions import generate_admin_keyboard

@require_admin
async def add_method(message: types.Message):
    await message.reply("Command to add payment method. Format: currency,label,name,address")

@require_admin
async def edit_method(message: types.Message):
    await message.reply("Command to edit payment method. Format: id,field,value")

@require_admin
async def delete_method(message: types.Message):
    await message.reply("Command to delete payment method. Format: id")

@require_admin
async def list_methods(message: types.Message):
    methods = list_payment_methods()
    lines = [f"{m['id']}: {m['currency']} - {m['label']} ({'Active' if m['is_active'] else 'Inactive'})" for m in methods]
    await message.reply("\n".join(lines) or "No payment methods found.")

@require_admin
async def set_admin_contact(message: types.Message):
    await message.reply("Command to set new admin. Format: username,user_id")

@require_admin
async def pending_payments(message: types.Message):
    requests = get_pending_requests()
    for r in requests:
        text = f"📩 Request ID: {r['id']}\nUser: @{r['username']}\nCurrency: {r['currency']}"
        keyboard = generate_admin_keyboard(r['id'])
        await message.reply(text, reply_markup=keyboard)