import io
import logging
from aiogram import types, Router, F
from aiogram.fsm.context import FSMContext
from services.payment_service import create_payment_request
from utils.file_manager import save_screenshot
from core.config import config
from bot.handlers.payment_flow import PaymentStates

router = Router()

@router.message(F.photo, PaymentStates.awaiting_screenshot)
async def handle_screenshot(message: types.Message, state: FSMContext):
    """
    Handles screenshot upload and notifies the CORRECT Admin Persona.
    """
    try:
        # 1. Pull the Persona Data from memory
        user_data = await state.get_data()
        currency = user_data.get("chosen_currency", "Unknown")
        # This is the Admin ID who owns the vault the user is in
        target_admin_id = user_data.get("method_owner_id") 

        # Fallback to Master Admin if for some reason the owner_id is missing
        if not target_admin_id:
            target_admin_id = config.ADMIN_USER_ID

        # 2. Get the photo
        photo = message.photo[-1]
        
        # 3. Download
        file_info = await message.bot.get_file(photo.file_id)
        file_io = await message.bot.download_file(file_info.file_path)
        raw_bytes = file_io.getvalue()
        
        # 4. Save to disk
        file_path = await save_screenshot(raw_bytes, f"{photo.file_id}.jpg")
        
        # 5. Create the request in your JSON
        username = message.from_user.username or message.from_user.full_name
        request = await create_payment_request(
            user_id=message.from_user.id,
            username=username,
            currency=currency,
            screenshot_path=file_path,
            owner_id=target_admin_id # Store who this request belongs to
        )
        
        # 6. Notify the SPECIFIC Admin Persona
        admin_msg = (
            f"📩 <b>New Payment Proof Received</b>\n"
            f"━━━━━━━━━━━━━━━\n"
            f"👤 <b>User:</b> @{username}\n"
            f"💰 <b>Currency:</b> {currency}\n"
            f"🆔 <b>Request ID:</b> <code>{request['id']}</code>\n"
            f"━━━━━━━━━━━━━━━\n"
            f"👉 Use /pending to review."
        )
        
        try:
            # We send the message to the target_admin_id (The Vault Owner)
            await message.bot.send_message(
                chat_id=target_admin_id, 
                text=admin_msg,
                parse_mode="HTML"
            )
            
            # OPTIONAL: Also notify Master Admin as a backup/monitor
            if target_admin_id != config.ADMIN_USER_ID:
                await message.bot.send_message(
                    chat_id=config.ADMIN_USER_ID,
                    text=f"📢 <i>Log: User @{username} sent proof to Admin {target_admin_id}</i>"
                )
                
        except Exception as e:
            logging.error(f"Failed to notify Admin {target_admin_id}: {e}")
        
        # 7. Clear the state
        await state.clear()
        
        # 8. Notify the user
        await message.reply(
            f"✅ <b>Screenshot received for {currency}!</b>\n"
            "Your payment is now being verified by the vault admin.",
            parse_mode="HTML"
        )

    except Exception as e:
        logging.error(f"Error in screenshot handler: {e}")
        await message.reply("❌ An error occurred while saving your screenshot. Please try again.")