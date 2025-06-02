from pycoingecko import CoinGeckoAPI
from datetime import datetime, timezone
import pandas as pd
from pprint import pprint


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


if __name__ == "__main__":
    # price = get_current_price(coin_id="ethereum", currency="rub")
    # print(price)

    data = get_history_data(coin_id="bitcoin", currency="rub", days=60)
    print(data)