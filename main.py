import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.redis import RedisStorage
from redis.asyncio import Redis
from config_reader import config
from handlers import common, menu, form

logging.basicConfig(level=logging.INFO)


async def main():
    redis_instance = Redis(
        host="redis-test-porem-578.db-msk0.amvera.tech",
        port=6379,
        password="bottest",
        ssl=True,
        ssl_cert_reqs=None
    )

    storage = RedisStorage(redis=redis_instance)

    bot = Bot(token=config.BOT_TOKEN.get_secret_value())

    dp = Dispatcher(storage=storage)

    dp.include_router(common.router)
    dp.include_router(menu.router)
    dp.include_router(form.router)

    await bot.delete_webhook(drop_pending_updates=True)

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
