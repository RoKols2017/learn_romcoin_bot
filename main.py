import asyncio

import aiogram
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

import config
from handlers import common, crypto_analyze


async def main():
    bot = Bot(token=config.TOKEN_TG)
    dp = Dispatcher()

    dp.include_router(common.router)
    dp.include_router(crypto_analyze.router)

    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())