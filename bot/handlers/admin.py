from aiogram import types, Router, F
from aiogram.filters import Command
from core.permissions import AdminFilter
from services.admin_service import (
    add_payment_method, edit_payment_method, 
    delete_payment_method, list_payment_methods, set_admin_contact
)
from services.verification_service import get_pending_requests, update_payment_status
from bot.keyboards.admin_actions import generate_admin_keyboard

router = Router()

# Apply AdminFilter to the entire router
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
    requests = await get_pending_requests()
    
    if not requests:
        await message.answer("☕ No pending payments at the moment.")
        return

    for r in requests:
        text = (
            f"📩 **Request ID:** {r['id']}\n"
            f"👤 **User:** @{r['username']}\n"
            f"💰 **Currency:** {r['currency']}"
        )
        keyboard = generate_admin_keyboard(r['id'])
        await message.reply(text, reply_markup=keyboard, parse_mode="Markdown")

async def handle_approve_decline(callback: types.CallbackQuery):
    """
    Handle admin clicking Approve or Decline buttons.
    """
    data = callback.data.split("_")
    action = data[0] # APPROVE or DECLINE
    request_id = data[1]
    
    is_approve = action == "APPROVE"
    
    success = await update_payment_status(
        request_id=request_id,
        admin_id=callback.from_user.id,
        approve=is_approve
    )
    
    if success:
        status_text = "✅ Approved" if is_approve else "❌ Declined"
        await callback.message.edit_text(
            f"{callback.message.text}\n\n**Status: {status_text}**",
            parse_mode="Markdown"
        )
        await callback.answer(f"Payment {status_text.lower()}!")
    else:
        await callback.answer("❌ Error updating payment status.", show_alert=True)
