from aiogram import Dispatcher
from aiogram.filters import Command
from bot.handlers import start, payment_flow, screenshot, admin

def setup_handlers(dp: Dispatcher):
    """
    Register all message and callback handlers for the bot.
    """
    # User commands
    dp.message.register(start.start_command, Command(commands=["start"]))

    # Screenshot uploads
    dp.message.register(screenshot.handle_screenshot, lambda m: m.photo is not None)

    # Admin commands
    dp.message.register(admin.add_method_handler, Command(commands=["add_method"]))
    dp.message.register(admin.edit_method_handler, Command(commands=["edit_method"]))
    dp.message.register(admin.delete_method_handler, Command(commands=["delete_method"]))
    dp.message.register(admin.list_methods_handler, Command(commands=["list_methods"]))
    dp.message.register(admin.set_admin_contact_handler, Command(commands=["set_contact"]))
    dp.message.register(admin.pending_payments_handler, Command(commands=["pending"]))

    # Callback query handlers (approve/decline)
    dp.callback_query.register(admin.handle_approve_decline, lambda c: c.data.startswith("APPROVE_"))
    dp.callback_query.register(admin.handle_approve_decline, lambda c: c.data.startswith("DECLINE_"))
