from aiogram import Router, types, F
from aiogram.filters import Command
from keyboards.main import get_start_keyboard
from keyboards.help import get_help_keyboard
from keyboards.currency import get_currency_keyboard
from keyboards.common import get_keyboard


router = Router()

@router.message(Command("start"))
async def cmd_start(message: types.Message):
    keyboard = get_start_keyboard()
    await message.answer(
        "Привет! Я бот для анализа криптовалют. Нажми /help, чтобы узнать, что я умею.",
        reply_markup=keyboard
    )


@router.message(Command("help"))
async def cmd_help(message: types.Message):
    keyboard = get_help_keyboard()
    await message.answer(
        "Доступные функции:",
        reply_markup=keyboard
    )

@router.message(F.text.in_(["/price", "/daily", "/analyze", "/alerts"]))
async def choose_currency(message: types.Message):
    command = message.text.lstrip("/")
    keyboard = get_keyboard(command)
    await message.answer(
        f"Выберите монету для команды {message.text}:",
        reply_markup=keyboard
    )
