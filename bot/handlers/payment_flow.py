from aiogram import types, Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from services.payment_service import get_active_currencies 
from services.admin_service import get_user_assigned_admin  

router = Router()

class PaymentStates(StatesGroup):
    awaiting_screenshot = State()

@router.callback_query(F.data.startswith("pay_"))
async def process_payment_selection(callback: types.CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    method_id = callback.data.split("_")[1]

    # 1. Identify which Admin this user is bound to
    assigned_admin_id = await get_user_assigned_admin(user_id)
    
    # 2. Get ONLY the currencies for THIS Admin Persona
    methods = await get_active_currencies(owner_id=assigned_admin_id)
    
    # 3. Find the specific method chosen
    selected_method = next((m for m in methods if str(m.get('id')) == method_id), None)

    if not selected_method:
        await callback.answer("❌ This method is not available in this vault.", show_alert=True)
        return

    # --- MEMORY LOGIC ---
    await state.update_data(
        chosen_currency=selected_method.get('currency'),
        method_owner_id=selected_method.get('owner_id'),
        # Optional: save amount to state if you want to use it in the review process later
        payment_amount=selected_method.get('amount', 'N/A') 
    )
    await state.set_state(PaymentStates.awaiting_screenshot)

    await callback.answer()

    label = selected_method.get('label', 'Payment Method')
    currency = selected_method.get('currency', '')
    name = selected_method.get('name', 'N/A')
    address = selected_method.get('address', 'N/A')
    amount = selected_method.get('amount', 'N/A') # <--- FIX: Extract the amount

    reply_text = (
        f"<b>💳 {currency} - {label}</b>\n\n"
        f"💰 <b>Amount to Send:</b> <code>{amount}</code>\n" # <--- FIX: Added to display
        f"👤 <b>Name:</b> <code>{name}</code>\n"
        f"🏦 <b>Account/Address:</b> <code>{address}</code>\n\n"
        f"━━━━━━━━━━━━━━━\n"
        f"✅ <b>Step 2:</b> Send exactly <code>{amount}</code>.\n"
        f"📸 <b>Step 3:</b> Upload the screenshot here.\n\n"
        f"<i>The bot is waiting for your photo...</i>"
    )

    await callback.message.edit_text(reply_text, parse_mode="HTML")