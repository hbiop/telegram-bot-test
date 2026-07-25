import asyncio
import logging
from aiogram import Bot, Dispatcher
from config_reader import config
from handlers import common, menu

logging.basicConfig(level=logging.INFO)


async def main():
    bot = Bot(token=config.BOT_TOKEN.get_secret_value())

    dp = Dispatcher()

    dp.include_router(common.router)
    dp.include_router(menu.router)

    await bot.delete_webhook(drop_pending_updates=True)

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())