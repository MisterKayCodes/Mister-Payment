from aiogram import Dispatcher
from aiogram.filters import Command
from bot.handlers import start, payment_flow, screenshot, admin

def register_handlers(dp: Dispatcher):
    # User commands
    dp.message.register(start.start_command, Command(commands=["start"]))

    # Screenshot handler
    dp.message.register(screenshot.handle_screenshot, content_types=["photo"])

    # Admin commands
    dp.message.register(admin.add_method, Command(commands=["add_method"]))
    dp.message.register(admin.edit_method, Command(commands=["edit_method"]))
    dp.message.register(admin.delete_method, Command(commands=["delete_method"]))
    dp.message.register(admin.list_methods, Command(commands=["list_methods"]))
    dp.message.register(admin.set_admin_contact, Command(commands=["set_admin_contact"]))
    dp.message.register(admin.pending_payments, Command(commands=["admin_pending"]))