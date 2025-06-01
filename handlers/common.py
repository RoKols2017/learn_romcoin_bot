from aiogram import Router, types
from aiogram.filters import Command


router = Router()

@router.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Привет, я бот который собирается обзавестись ИИ. Напиши /help, чтобы узнать, что я умею.")


@router.message(Command("help"))
async def cmd_help(message: types.Message):
    await message.answer("""Скоро я буду уметь:
    - Получать цены активов.
    - Анализировать рынок.
    - Строить графики.
    - Работать с файлами.""")
