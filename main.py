import asyncio
import sys
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from core.config import config  # Using the instance you created in config.py
from utils.logger import logger, setup_logger

# 1. Initialize Logger
setup_logger(config.LOG_DIR)

async def main():
    # 2. Initialize Bot with modern properties
    # Defaulting to HTML parse mode makes your 💰 and <b>bold</b> text work automatically
    bot = Bot(
        token=config.BOT_TOKEN,
        default_bot_properties=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )

    # 3. Initialize Dispatcher
    dp = Dispatcher()

    # 4. Import and Include Routers
    # Assuming you've moved handlers to routers as we discussed earlier
    from bot.handlers.admin import router as admin_router
    from bot.handlers.user import router as user_router
    
    dp.include_router(admin_router)
    dp.include_router(user_router)

    # 5. Start Polling
    try:
        logger.info("🚀 Mister Payment Bot is starting...")
        
        # This line clears any messages sent while the bot was offline 
        # so you don't get spammed on startup
        await bot.delete_webhook(drop_pending_updates=True)
        
        await dp.start_polling(bot)
    except Exception as e:
        logger.error(f"❌ Critical error: {e}")
    finally:
        # 6. Graceful Shutdown
        logger.info("💤 Bot is shutting down...")
        await bot.session.close()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("👋 Bot stopped by user.")