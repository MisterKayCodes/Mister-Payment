from aiogram import Dispatcher
from bot.handlers import start, payment_flow, screenshot, admin

def register_handlers(dp: Dispatcher):
    # User commands
    dp.message.register(start.start_command, commands=["start"])
    dp.message.register(payment_flow.currency_selection, lambda m: True)
    dp.message.register(screenshot.handle_screenshot, content_types=["photo"])
    
    # Admin commands
    dp.message.register(admin.add_method, commands=["add_method"])
    dp.message.register(admin.edit_method, commands=["edit_method"])
    dp.message.register(admin.delete_method, commands=["delete_method"])
    dp.message.register(admin.list_methods, commands=["list_methods"])
    dp.message.register(admin.set_admin_contact, commands=["set_admin_contact"])
    dp.message.register(admin.pending_payments, commands=["admin_pending"])