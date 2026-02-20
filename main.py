import asyncio
from aiogram import Bot, Dispatcher
from core.config import Config
from bot.router import setup_handlers
from utils.logger import setup_logger, logger

# Load config and setup logging
config = Config()
setup_logger(config.LOG_DIR)

async def main():
    """
    Entry point for Mister Payment bot.
    """
    print("Starting Mister Payment bot...")
    try:
        async with Bot(token=config.BOT_TOKEN) as bot:
            dp = Dispatcher()

            # Register all handlers
            setup_handlers(dp)

            # Start polling
            await dp.start_polling(bot)
    except Exception as e:
        logger.exception(f"Bot crashed: {e}")

if __name__ == "__main__":
    asyncio.run(main())