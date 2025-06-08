from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from utils.coingecko_service import (
    get_current_price_async, 
    get_history_data_async, 
    get_daily_summary_async,
    get_market_indicators_async,
    get_price_alerts_async,
    format_number
)


router = Router()


@router.message(F.text.startswith("/price"))
async def get_price(message: Message):
    """Обработчик команды /price coin_id для получения текущей цены"""

    parts = message.text.strip().split()
    if len(parts) < 2:
        popular = [
            ("bitcoin", "₿"),
            ("ethereum", "Ξ"),
            ("solana", "◎"),
            ("dogecoin", "Ð")
        ]
        keyboard = ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text=f"/price {coin}") for coin, emoji in popular[i:i+2]]
                for i in range(0, len(popular), 2)
            ],
            resize_keyboard=True
        )
        await message.reply(
            "Выбери монету для анализа или введи команду в формате /price [монета]",
            reply_markup=keyboard
        )
        return

    coin_id = parts[1].lower().strip()

    price = await get_current_price_async(coin_id)
    if price is None:
        await message.reply(f"Монета с id {coin_id} не найдена")
        return

    await message.reply(f"💰 Текущая цена {coin_id}: ${format_number(price)} USD")


@router.message(F.text.startswith("/daily"))
async def daily_summary(message: Message):
    """Обработчик команды /daily coin_id для получения дневной сводки"""
    
    parts = message.text.strip().split()
    if len(parts) < 2:
        popular = [
            ("bitcoin", "₿"),
            ("ethereum", "Ξ"),
            ("solana", "◎"),
            ("dogecoin", "Ð")
        ]
        keyboard = ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text=f"/daily {coin}") for coin, emoji in popular[i:i+2]]
                for i in range(0, len(popular), 2)
            ],
            resize_keyboard=True
        )
        await message.reply(
            "Выбери монету для анализа или введи команду в формате /daily [монета]",
            reply_markup=keyboard
        )
        return

    coin_id = parts[1].lower().strip()
    
    summary = await get_daily_summary_async(coin_id)
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
        popular = [
            ("bitcoin", "₿"),
            ("ethereum", "Ξ"),
            ("solana", "◎"),
            ("dogecoin", "Ð")
        ]
        keyboard = ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text=f"/analyze {coin}") for coin, emoji in popular[i:i+2]]
                for i in range(0, len(popular), 2)
            ],
            resize_keyboard=True
        )
        await message.reply(
            "Выбери монету для анализа или введи команду в формате /analyze [монета]",
            reply_markup=keyboard
        )
        return

    coin_id = parts[1].lower().strip()
    
    indicators = await get_market_indicators_async(coin_id)
    if indicators is None:
        await message.reply(f"Не удалось получить данные для монеты {coin_id}")
        return
    
    response = f"📊 Анализ {coin_id}:\n\n"
    response += f"💰 Текущая цена: ${format_number(indicators['current_price'])}\n"
    response += f"📊 Средняя цена: ${format_number(indicators['average_price'])}\n"
    response += f"📈 Изменение цены: {format_number(indicators['price_change'])}%\n"
    response += f"📊 Волатильность: {format_number(indicators['volatility_percent'])}%\n"
    response += f"💹 SMA: ${format_number(indicators['sma'])}\n"
    response += f"💹 EMA: ${format_number(indicators['ema']) if indicators['ema'] is not None else 'N/A'}\n"
    response += f"📈 RSI: {format_number(indicators['rsi']) if indicators['rsi'] is not None else 'N/A'}\n"
    # Сигналы по RSI и EMA
    signal = None
    if indicators['rsi'] is not None and indicators['ema'] is not None:
        if indicators['rsi'] < 30 and indicators['current_price'] > indicators['ema']:
            signal = '🟢 Сигнал на покупку (RSI < 30 и цена > EMA)'
        elif indicators['rsi'] > 70 and indicators['current_price'] < indicators['ema']:
            signal = '🔴 Сигнал на продажу (RSI > 70 и цена < EMA)'
        else:
            signal = '⚪️ Явного сигнала нет (сидеть на заборе/наблюдать)'
    else:
        signal = '⚪️ Недостаточно данных для сигнала (RSI/EMA)'
    response += f"\n{signal}\n"
    response += f"📊 Средний объем: ${format_number(indicators['average_volume'])}\n"
    response += f"📈 Максимальный объем: ${format_number(indicators['max_volume'])}"
    
    await message.reply(response)


@router.message(F.text.startswith("/alerts"))
async def price_alerts(message: Message):
    """Обработчик команды /alerts coin_id для получения торговых сигналов"""
    
    parts = message.text.strip().split()
    if len(parts) < 2:
        popular = [
            ("bitcoin", "₿"),
            ("ethereum", "Ξ"),
            ("solana", "◎"),
            ("dogecoin", "Ð")
        ]
        keyboard = ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text=f"/alerts {coin}") for coin, emoji in popular[i:i+2]]
                for i in range(0, len(popular), 2)
            ],
            resize_keyboard=True
        )
        await message.reply(
            "Выбери монету для анализа или введи команду в формате /alerts [монета]",
            reply_markup=keyboard
        )
        return

    coin_id = parts[1].lower().strip()
    
    analysis = await get_price_alerts_async(coin_id)
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