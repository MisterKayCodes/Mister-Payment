import logging
import os
from aiogram import types, Router, F
from aiogram.filters import Command
from aiogram.types import FSInputFile 
from core.enums import PaymentReviewCallback, CallbackActions
from core.permissions import AdminFilter
from core.config import config
from services.admin_service import (
    add_payment_method, 
    edit_payment_method, 
    delete_payment_method, 
    list_payment_methods, 
    set_admin_contact, 
    get_bot_config, 
    update_bot_config,
    register_vault_code,     # <--- ADD THIS
    get_admin_id_by_code,    # <--- ADD THIS
    bind_user_to_admin,      
    get_user_assigned_admin  
)
from services.verification_service import get_pending_requests, update_payment_status
from bot.keyboards.admin_actions import generate_admin_keyboard

router = Router()
router.message.filter(AdminFilter())

# --- ADMIN MENU ---

@router.message(Command("admin"))
async def admin_menu(message: types.Message):
    menu_text = (
        "<b>🛠 Admin Control Panel</b>\n\n"
        "📩 /pending - View pending proof of payments\n"
        "📜 /list_methods - View all payment methods\n"
        "➕ /add_method - Add a new payment method\n"
        "✏️ /edit_method - Edit a method (ID, Field, Value)\n"
        "🗑️ /delete_method - Delete a method (ID)\n"
        "🔗 /set_link - Set the delivery link for users\n"
        "👤 /set_contact - Update admin contact info\n"
        "👑 /register_vault - Create a new vault persona with a unique code\n"
        "👑 /promote - Promote a user to Admin Persona (Master Admin only)"
    )
    await message.answer(menu_text, parse_mode="HTML")
# --- METHOD MANAGEMENT ---

@router.message(Command("add_method"))
async def process_add_method(message: types.Message):
    try:
        admin_id = message.from_user.id 
        content = message.text.replace("/add_method", "").strip()
        if not content: raise ValueError()
        
        # UPDATED: Now expecting 5 fields (added amount)
        parts = [i.strip() for i in content.split(",")]
        if len(parts) < 5:
            return await message.reply("❌ <b>Missing fields!</b> Use: currency,label,name,address,amount")

        currency, label, name, address, amount = parts
        
        # We pass admin_id and the new amount to the service
        new_method = await add_payment_method(
            owner_id=admin_id,
            currency=currency, 
            label=label, 
            name=name, 
            address=address,
            amount=amount  # <--- New field
        )
        await message.reply(
            f"✅ <b>Method Added to your Vault!</b>\n"
            f"💰 Price: <code>{amount}</code>\n"
            f"🆔 ID: <code>{new_method['id']}</code>"
        )
    except Exception as e:
        logging.error(f"Error adding method: {e}")
        await message.reply("❌ <b>Format:</b> <code>/add_method currency,label,name,address,amount</code>")

        
@router.message(Command("edit_method"))
async def process_edit_method(message: types.Message):
    try:
        content = message.text.replace("/edit_method", "").strip()
        method_id, field, value = [i.strip() for i in content.split(",")]
        success = await edit_payment_method(method_id, field, value)
        if success:
            await message.reply(f"✅ Method <code>{method_id}</code> updated!")
        else:
            await message.reply("❌ Method ID not found.")
    except Exception:
        await message.reply("❌ <b>Format:</b> <code>/edit_method id,field,value</code>")


@router.message(Command("list_methods"))
async def list_methods_handler(message: types.Message):
    all_methods = await list_payment_methods()
    # Filter to only show methods owned by the person asking
    my_methods = [m for m in all_methods if str(m.get('owner_id')) == str(message.from_user.id)]
    
    if not my_methods:
        return await message.answer("No methods found in your vault.")
    
    lines = [f"🆔 <code>{m['id']}</code>: {m['currency']} ({m['label']})" for m in my_methods]
    await message.answer("<b>Your Vault Methods:</b>\n" + "\n".join(lines), parse_mode="HTML")


@router.message(Command("delete_method"))
async def process_delete_method(message: types.Message):
    """
    Format: /delete_method [ID]
    """
    try:
        # Extract the ID after the command
        method_id = message.text.replace("/delete_method", "").strip()
        
        if not method_id:
            return await message.reply("❌ Please provide an ID. Usage: <code>/delete_method 8f2a1b</code>")

        # Call the service we verified earlier
        success = await delete_payment_method(method_id)
        
        if success:
            await message.reply(f"🗑️ <b>Method Deleted!</b>\nID: <code>{method_id}</code> has been removed.")
        else:
            await message.reply("❌ <b>Error:</b> Method ID not found. Check /list_methods for the correct ID.")
            
    except Exception as e:
        logging.error(f"Error deleting method: {e}")
        await message.reply("❌ An error occurred while trying to delete the method.")

# --- DELIVERY LINK CONFIG ---

@router.message(Command("set_link"))
async def set_success_link(message: types.Message):
    """Sets the link users get after approval"""
    args = message.text.split(maxsplit=1)
    if len(args) < 2:
        return await message.reply("❌ Usage: <code>/set_link https://t.me/yourlink</code>")

    new_link = args[1].strip()
    await update_bot_config(success_link=new_link)
    await message.reply(f"✅ <b>Success!</b> Link saved:\n<code>{new_link}</code>")

# --- VERIFICATION SYSTEM ---

@router.message(Command("pending"))
async def pending_payments(message: types.Message):
    """
    Shows pending payments belonging ONLY to the admin who sends the command.
    """
    admin_id = message.from_user.id
    
    # 1. Fetch all pending requests
    all_requests = await get_pending_requests()
    
    # 2. Filter requests to only show those belonging to THIS admin's vault
    # We check if owner_id matches the admin_id
    vault_requests = [
        r for r in all_requests 
        if str(r.get('owner_id')) == str(admin_id)
    ]
    
    if not vault_requests:
        await message.answer("☕ No pending payments in your vault at the moment.")
        return

    for r in vault_requests:
        text = (
            f"📩 <b>New Payment Proof (Your Vault)</b>\n"
            f"━━━━━━━━━━━━━━━\n"
            f"🆔 <b>Request ID:</b> <code>{r['id']}</code>\n"
            f"👤 <b>User:</b> @{r.get('username', 'N/A')}\n"
            f"💰 <b>Currency:</b> {r['currency']}\n"
            f"━━━━━━━━━━━━━━━"
        )
        kb = generate_admin_keyboard(r['id'])
        path = r.get('screenshot_path')

        # Send photo if it exists
        if path and os.path.exists(path):
            await message.answer_photo(
                photo=FSInputFile(path), 
                caption=text, 
                reply_markup=kb, 
                parse_mode="HTML"
            )
        else:
            await message.answer(
                text + "\n⚠️ <i>Screenshot missing on server</i>", 
                reply_markup=kb, 
                parse_mode="HTML"
            )

            
# --- CALLBACK HANDLER ---

@router.callback_query(PaymentReviewCallback.filter())
async def handle_approve_decline(callback: types.CallbackQuery, callback_data: PaymentReviewCallback):
    action = callback_data.action
    request_id = callback_data.request_id
    is_approve = (action == CallbackActions.APPROVE)

    # A. Get user_id before updating status
    pending_reqs = await get_pending_requests()
    target_user_id = next((r['user_id'] for r in pending_reqs if r['id'] == request_id), None)

    # B. Update Status
    success = await update_payment_status(request_id, callback.from_user.id, is_approve)
    
    if success:
        # C. Deliver link to user if approved
        if is_approve and target_user_id:
            bot_cfg = await get_bot_config()
            delivery_link = bot_cfg.get("success_link", "Contact admin for access.")
            
            try:
                await callback.bot.send_message(
                    chat_id=target_user_id,
                    text=f"✅ <b>Payment Approved!</b>\n\nYour access link is:\n{delivery_link}",
                    parse_mode="HTML"
                )
            except Exception as e:
                logging.error(f"Failed to DM user {target_user_id}: {e}")

        # Update Admin UI
        status_emoji = "✅ Approved" if is_approve else "❌ Declined"
        original_text = callback.message.caption or callback.message.text
        new_text = f"{original_text}\n\n<b>Status: {status_emoji}</b>"
        
        if callback.message.caption:
            await callback.message.edit_caption(caption=new_text, parse_mode="HTML")
        else:
            await callback.message.edit_text(text=new_text, parse_mode="HTML")
            
        await callback.answer(f"Payment {action.value}d!")
    else:
        await callback.answer("❌ Error: Request not found.", show_alert=True)

@router.message(Command("register_vault"))
async def cmd_register_vault(message: types.Message):
    """
    Format: /register_vault MYNAME
    """
    args = message.text.split()
    if len(args) < 2:
        return await message.reply("❌ Usage: <code>/register_vault [UNIQUE_NAME]</code>")

    vault_code = args[1].upper()
    admin_id = message.from_user.id

    # Save the link between this user and this code
    await register_vault_code(admin_id, vault_code)

    # Generate their personal invite link
    bot_info = await message.bot.get_me()
    share_link = f"https://t.me/{bot_info.username}?start={vault_code}"

    await message.reply(
        f"👑 <b>Vault Persona Created!</b>\n\n"
        f"Your Code: <code>{vault_code}</code>\n"
        f"Your Personal Link: <code>{share_link}</code>\n\n"
        "Users who join via this link will only see <b>YOUR</b> payment methods."
    )

@router.message(Command("promote"))
async def promote_to_admin(message: types.Message):
    # ONLY the Master Admin from .env can promote others
    if message.from_user.id != config.ADMIN_USER_ID:
        return

    args = message.text.split()
    if len(args) < 2:
        return await message.reply("❌ Usage: <code>/promote [USER_ID]</code>")

    new_admin_id = args[1].strip()
    
    # Save this ID to your bot_config.json under an 'admins' list
    data = await get_bot_config()
    if "authorized_admins" not in data:
        data["authorized_admins"] = []
    
    if int(new_admin_id) not in data["authorized_admins"]:
        data["authorized_admins"].append(int(new_admin_id))
        await update_bot_config(authorized_admins=data["authorized_admins"])
        await message.reply(f"👑 User <code>{new_admin_id}</code> is now an Admin Persona!")
    else:
        await message.reply("ℹ️ This user is already an admin.")

# --- ADMIN CONTACT CONFIG ---

@router.message(Command("set_contact"))
async def set_admin_contact_handler(message: types.Message):
    """
    Sets the contact username or link (e.g., @MySupport) 
    that users see if they have issues.
    """
    args = message.text.split(maxsplit=1)
    if len(args) < 2:
        return await message.reply("❌ Usage: <code>/set_contact @YourUsername</code>")

    new_contact = args[1].strip()
    
    # Save to the bot config
    await update_bot_config(admin_contact=new_contact)
    
    await message.reply(
        f"👤 <b>Contact Updated!</b>\n"
        f"Users will now see: <code>{new_contact}</code> if they need help."
    )