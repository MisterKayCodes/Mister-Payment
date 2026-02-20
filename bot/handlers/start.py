import os
import logging
from aiogram import types, Router
from aiogram.filters import CommandStart, CommandObject

from bot.keyboards.payment_methods import generate_payment_keyboard
from services.payment_service import get_active_currencies, get_user_payment_status
from services.admin_service import get_admin_id_by_code, bind_user_to_admin, get_user_assigned_admin
from core.config import config
from core.enums import PaymentStatus
from core.permissions import AdminFilter  # Imported for the admin check

router = Router()

@router.message(CommandStart())
async def start_command(message: types.Message, command: CommandObject):
    try:
        user_id = message.from_user.id
        vault_code = command.args

        # 1. Handle Vault Entry (Link check)
        if vault_code:
            admin_id = await get_admin_id_by_code(vault_code)
            if admin_id:
                await bind_user_to_admin(user_id, admin_id)
                await message.answer(f"🔓 <b>Vault Unlocked!</b>\nYou are now connected to the <b>{vault_code}</b> persona.")
            else:
                await message.answer("❌ Invalid Vault Code. Please check your link.")
                return

        # 2. Identify which Admin Persona this user sees
        assigned_admin_id = await get_user_assigned_admin(user_id)
        
        # Check if the user is an admin (Master or Crowned)
        is_admin = await AdminFilter().__call__(message)
        
        # If no link found, and it's not an admin, they see the gatekeeper message
        if not assigned_admin_id and not is_admin:
            await message.answer("👋 Welcome! Please join via a valid admin invite link to see payment methods.")
            return

        # 3. Admin Greeting
        if is_admin:
            status_label = "Master Admin" if user_id == config.ADMIN_USER_ID else "Admin Persona"
            await message.answer(f"🛠 <b>{status_label} Access</b>\nUse /admin to manage your vault.", parse_mode="HTML")

        # 4. Check for pending transaction
        last_request = await get_user_payment_status(user_id)
        pending_note = ""
        if last_request and last_request.get("status") == PaymentStatus.PENDING.value:
            pending_note = "\n\n⏳ <b>Notice:</b> Your payment proof is <b>under review</b>."

        # 5. Get currencies filtered by the OWNER (The Persona)
        # Admins see their own methods by default if they haven't used a link
        target_owner = assigned_admin_id if assigned_admin_id else user_id
        currencies = await get_active_currencies(owner_id=target_owner)
        
        if not currencies:
            if not is_admin:
                await message.answer("❌ This vault currently has no active payment methods.")
            return

        keyboard = generate_payment_keyboard(currencies)
        text = (
            f"👋 Hello, {message.from_user.first_name}!\n"
            "💰 Please select a payment method from this vault:"
            f"{pending_note}"
        )
        
        await message.answer(text, reply_markup=keyboard, parse_mode="HTML")

    except Exception as e:
        logging.error(f"Error in start_command: {e}")
        await message.answer("⚠️ An error occurred. Please restart with /start")