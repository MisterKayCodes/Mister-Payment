import asyncio
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import BotCommand

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
    logger.info("Starting Mister Payment bot...")
    
    # 1. Initialize Bot with default HTML parsing
    bot = Bot(
        token=config.BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )

    # 2. Initialize Dispatcher with MemoryStorage (Crucial for FSM)
    # This allows the bot to remember the currency selected across messages
    dp = Dispatcher(storage=MemoryStorage())

    try:
        # 3. Register all handlers (Start, Payment, Screenshot, Admin, Help)
        setup_handlers(dp)

        # 4. Set the Telegram Menu Commands
        await bot.set_my_commands([
            BotCommand(command="start", description="Start payment process"),
            BotCommand(command="help", description="How to use the bot"),
            BotCommand(command="admin", description="Admin panel (Admins only)")
        ])

        # 5. Clean start: ignore old messages sent while bot was offline
        await bot.delete_webhook(drop_pending_updates=True)

        # 6. Start polling
        await dp.start_polling(bot)
        
    except Exception as e:
        logger.exception(f"Bot crashed: {e}")
    finally:
        # 7. Ensure the bot session is closed properly to avoid errors on exit
        await bot.session.close()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Bot stopped manually.")