from pycoingecko import CoinGeckoAPI
from datetime import datetime, timezone
import pandas as pd
import numpy as np
from pprint import pprint
import asyncio


def format_number(number: float, decimals: int = 2) -> str:
    """Форматирование числа с разделением разрядов"""
    if number is None:
        return "N/A"
    if number >= 1_000_000_000:  # миллиарды
        return f"{number/1_000_000_000:,.{decimals}f}B"
    if number >= 1_000_000:  # миллионы
        return f"{number/1_000_000:,.{decimals}f}M"
    if number >= 1_000:  # тысячи
        return f"{number:,.{decimals}f}"
    return f"{number:.{decimals}f}"


#pd.set_option('display.float_format', '{:.2f}'.format) # Два знака после запятой
cg = CoinGeckoAPI()


def get_current_price(coin_id: str, currency: str = "usd"):
    """Получить текущую цену монеты с CoinGecko."""
    try:
        data = cg.get_price(ids=coin_id, vs_currencies=currency)
    except Exception as e:
        print(f"Ошибка при запросе данных к CoinGecko - {e}")
        return None
    if coin_id in data and currency in data.get(coin_id):
        return data.get(coin_id).get(currency)
    else:
        return None


def get_history_data(coin_id: str, currency: str = "usd", days: int = 60):
    """Получить исторические данные по монете."""
    try:
        data = cg.get_coin_market_chart_by_id(id=coin_id, vs_currency=currency, days=days)
    except Exception as e:
        print(f"Ошибка при запросе данных к CoinGecko - {e}")
        return None

    if 'prices' not in data or 'total_volumes' not in data:
        print("Нет нужных данных в ответе")
        return None


    prices = data.get("prices")
    volumes = data.get("total_volumes")

    date_list = []
    prices_list = []
    volumes_list = []


    for price, volume in zip(prices, volumes):
        timestamp = price[0] / 1000
        dt = datetime.fromtimestamp(timestamp, tz=timezone.utc)
        date_list.append(dt)
        prices_list.append(price[1])
        volumes_list.append(volume[1])

    df = pd.DataFrame({'date': date_list, 'price': prices_list, 'volume': volumes_list})

    return df


def get_daily_summary(coin_id: str, currency: str = "usd"):
    """Функция для краткого отчета за сутки"""
    df = get_history_data(coin_id=coin_id, currency=currency, days=1)
    if df is None or len(df) == 0:
        return None

    current_price = df["price"].iloc[-1]
    min_price = df["price"].min()
    max_price = df["price"].max()
    total_volume = df["volume"].sum()

    summary = {
        "current_price": current_price,
        "min_price": min_price,
        "max_price": max_price,
        "total_volume": total_volume,
    }

    return summary


def calculate_price_change(df: pd.DataFrame) -> dict:
    """Расчет изменения цены в процентах"""
    if df is None or len(df) < 2:
        return None
    
    first_price = df['price'].iloc[0]
    last_price = df['price'].iloc[-1]
    
    price_change = ((last_price - first_price) / first_price) * 100
    
    return {
        'price_change_percent': price_change,
        'start_price': first_price,
        'end_price': last_price
    }

def calculate_ema(prices: pd.Series, span: int = 14) -> float:
    if prices is None or len(prices) < span:
        return None
    return prices.ewm(span=span, adjust=False).mean().iloc[-1]

def calculate_rsi(prices: pd.Series, period: int = 14) -> float:
    if prices is None or len(prices) < period + 1:
        return None
    delta = prices.diff()
    gain = delta.where(delta > 0, 0.0)
    loss = -delta.where(delta < 0, 0.0)
    avg_gain = gain.rolling(window=period, min_periods=period).mean()
    avg_loss = loss.rolling(window=period, min_periods=period).mean()
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi.iloc[-1]

def get_market_indicators(coin_id: str, currency: str = "usd", days: int = 1):
    """Получение расширенных рыночных показателей"""
    df = get_history_data(coin_id=coin_id, currency=currency, days=days)
    if df is None or len(df) == 0:
        return None
        
    # Базовые показатели
    current_price = df["price"].iloc[-1]
    avg_price = df["price"].mean()
    price_std = df["price"].std()  # Стандартное отклонение цены
    
    # Объемы
    avg_volume = df["volume"].mean()
    max_volume = df["volume"].max()
    
    # Волатильность (на основе стандартного отклонения)
    volatility = (price_std / avg_price) * 100
    
    # Изменение цены
    price_changes = calculate_price_change(df)
    
    # Расчет простой скользящей средней (SMA)
    sma = df["price"].rolling(window=min(len(df), 6)).mean().iloc[-1]
    
    # Расчет EMA
    ema = calculate_ema(df["price"], span=14)
    
    # Расчет RSI
    rsi = calculate_rsi(df["price"], period=14)
    
    return {
        "current_price": current_price,
        "average_price": avg_price,
        "price_std": price_std,
        "volatility_percent": volatility,
        "average_volume": avg_volume,
        "max_volume": max_volume,
        "sma": sma,
        "ema": ema,
        "rsi": rsi,
        "price_change": price_changes["price_change_percent"] if price_changes else None
    }

def get_price_alerts(coin_id: str, currency: str = "usd", volatility_threshold: float = 5.0) -> dict:
    """Анализ цены и генерация торговых сигналов"""
    indicators = get_market_indicators(coin_id, currency)
    if indicators is None:
        return None
        
    alerts = []
    
    # Проверка волатильности
    if indicators["volatility_percent"] > volatility_threshold:
        alerts.append(f"⚠️ Высокая волатильность: {indicators['volatility_percent']:.2f}%")
    
    # Анализ цены относительно SMA
    if indicators["current_price"] > indicators["sma"]:
        alerts.append("📈 Цена выше SMA - возможный восходящий тренд")
    elif indicators["current_price"] < indicators["sma"]:
        alerts.append("📉 Цена ниже SMA - возможный нисходящий тренд")
    
    # Анализ объема
    if indicators["max_volume"] > indicators["average_volume"] * 2:
        alerts.append("📊 Обнаружен высокий объем торгов")
    
    return {
        "indicators": indicators,
        "alerts": alerts
    }

async def get_current_price_async(*args, **kwargs):
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(None, get_current_price, *args, **kwargs)

async def get_history_data_async(*args, **kwargs):
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(None, get_history_data, *args, **kwargs)

async def get_daily_summary_async(*args, **kwargs):
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(None, get_daily_summary, *args, **kwargs)

async def get_market_indicators_async(*args, **kwargs):
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(None, get_market_indicators, *args, **kwargs)

async def get_price_alerts_async(*args, **kwargs):
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(None, get_price_alerts, *args, **kwargs)

if __name__ == "__main__":
    # price = get_current_price(coin_id="ethereum", currency="rub")
    # print(price)

    data = get_history_data(coin_id="bitcoin", currency="rub", days=60)
    print(data)