from aiogram import Router, F
from aiogram.types import Message
from utils.coingecko_service import get_current_price, get_history_data


router = Router()


@router.message(F.text.startswith("/analyze"))
async def analyze_crypto(message: Message):
    """Обработчик команды /analyze coin_is"""

    parts = message.text.strip().split()
    if len(parts) < 2:
        await message.reply("Введите команду в виде: /analyze bitcoin")
        return

    coin_id = parts[1].lower().strip()

    price = get_current_price(coin_id)
    if price is None:
        await message.reply(f"Монета с id {coin_id} не найдена")
        return

    await message.reply(f"Текущая цена {coin_id}: {price} usd")