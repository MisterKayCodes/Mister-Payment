import asyncio
from aiogram import Bot, Dispatcher
from core.config import Config
from bot.router import register_handlers
from utils.logger import setup_logger

config = Config()
setup_logger(config.LOG_DIR)

bot = Bot(token=config.BOT_TOKEN)
dp = Dispatcher()

register_handlers(dp)

async def main():
    try:
        print("Starting Mister Payment bot...")
        await dp.start_polling(bot)
    finally:
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run(main())