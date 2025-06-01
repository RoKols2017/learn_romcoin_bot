import asyncio

import aiogram
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

import config
from handlers import common


async def main():
    bot = Bot(token=config.TOKEN_TG)
    dp = Dispatcher()

    dp.include_router(common.router)

    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())