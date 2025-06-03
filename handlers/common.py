from aiogram import Router, types
from aiogram.filters import Command


router = Router()

@router.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Привет, я бот который собирается обзавестись ИИ. Напиши /help, чтобы узнать, что я умею.")


@router.message(Command("help"))
async def cmd_help(message: types.Message):
    await message.answer("""Доступные команды:
    /price [монета] - получить текущую цену криптовалюты
    /daily [монета] - получить дневную сводку по криптовалюте (мин/макс цена, объем)
    /analyze [монета] - полный анализ криптовалюты (тренды, волатильность, объемы)
    /alerts [монета] - получить торговые сигналы и предупреждения
    
Скоро я буду уметь:
    - Строить графики
    - Работать с файлами
    - Отслеживать несколько монет одновременно""")
