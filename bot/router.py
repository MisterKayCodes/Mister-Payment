from aiogram import Dispatcher
from bot.handlers import start, payment_flow, screenshot, admin, help

def setup_handlers(dp: Dispatcher):
    """
    Final optimized router order for Aiogram 3.x
    """

    # 1. Admin Handlers (Top priority)
    dp.include_router(admin.router)

    # 2. Start Handler (Priority 2 - Move this UP!)
    # This ensures /start is caught immediately
    dp.include_router(start.router)

    # 3. Help Handler
    dp.include_router(help.router)

    # 4. Payment Flow & Screenshots (Low priority/Greedy handlers)
    # These often wait for generic text/photos, so they must come last
    dp.include_router(payment_flow.router)
    dp.include_router(screenshot.router)