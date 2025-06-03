from aiogram import Router, F
from aiogram.types import Message
from utils.coingecko_service import (
    get_current_price, 
    get_history_data, 
    get_daily_summary,
    get_market_indicators,
    get_price_alerts,
    format_number
)


router = Router()


@router.message(F.text.startswith("/price"))
async def get_price(message: Message):
    """Обработчик команды /price coin_id для получения текущей цены"""

    parts = message.text.strip().split()
    if len(parts) < 2:
        await message.reply("Введите команду в виде: /price bitcoin")
        return

    coin_id = parts[1].lower().strip()

    price = get_current_price(coin_id)
    if price is None:
        await message.reply(f"Монета с id {coin_id} не найдена")
        return

    await message.reply(f"💰 Текущая цена {coin_id}: ${format_number(price)} USD")


@router.message(F.text.startswith("/daily"))
async def daily_summary(message: Message):
    """Обработчик команды /daily coin_id для получения дневной сводки"""
    
    parts = message.text.strip().split()
    if len(parts) < 2:
        await message.reply("Введите команду в виде: /daily bitcoin")
        return

    coin_id = parts[1].lower().strip()
    
    summary = get_daily_summary(coin_id)
    if summary is None:
        await message.reply(f"Не удалось получить данные для монеты {coin_id}")
        return
    
    response = f"📊 Дневная сводка по {coin_id}:\n\n"
    response += f"💰 Текущая цена: ${format_number(summary['current_price'])}\n"
    response += f"📉 Минимальная цена: ${format_number(summary['min_price'])}\n"
    response += f"📈 Максимальная цена: ${format_number(summary['max_price'])}\n"
    response += f"📊 Общий объем торгов: ${format_number(summary['total_volume'])}"
    
    await message.reply(response)


@router.message(F.text.startswith("/analyze"))
async def analyze_market(message: Message):
    """Обработчик команды /analyze coin_id для получения расширенного анализа"""
    
    parts = message.text.strip().split()
    if len(parts) < 2:
        await message.reply("Введите команду в виде: /analyze bitcoin")
        return

    coin_id = parts[1].lower().strip()
    
    indicators = get_market_indicators(coin_id)
    if indicators is None:
        await message.reply(f"Не удалось получить данные для монеты {coin_id}")
        return
    
    response = f"📊 Анализ {coin_id}:\n\n"
    response += f"💰 Текущая цена: ${format_number(indicators['current_price'])}\n"
    response += f"📊 Средняя цена: ${format_number(indicators['average_price'])}\n"
    response += f"📈 Изменение цены: {format_number(indicators['price_change'])}%\n"
    response += f"📊 Волатильность: {format_number(indicators['volatility_percent'])}%\n"
    response += f"💹 SMA: ${format_number(indicators['sma'])}\n"
    response += f"📊 Средний объем: ${format_number(indicators['average_volume'])}\n"
    response += f"📈 Максимальный объем: ${format_number(indicators['max_volume'])}"
    
    await message.reply(response)


@router.message(F.text.startswith("/alerts"))
async def price_alerts(message: Message):
    """Обработчик команды /alerts coin_id для получения торговых сигналов"""
    
    parts = message.text.strip().split()
    if len(parts) < 2:
        await message.reply("Введите команду в виде: /alerts bitcoin")
        return

    coin_id = parts[1].lower().strip()
    
    analysis = get_price_alerts(coin_id)
    if analysis is None:
        await message.reply(f"Не удалось получить данные для монеты {coin_id}")
        return
    
    indicators = analysis["indicators"]
    alerts = analysis["alerts"]
    
    response = f"🚨 Торговые сигналы для {coin_id}:\n\n"
    
    if alerts:
        response += "\n".join(alerts)
    else:
        response += "📊 Нет активных сигналов"
    
    response += f"\n\n💰 Текущая цена: ${format_number(indicators['current_price'])}"
    
    await message.reply(response)