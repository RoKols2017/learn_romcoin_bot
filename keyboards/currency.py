from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

POPULAR_COINS = [
    ("bitcoin", "₿"),
    ("ethereum", "Ξ"),
    ("solana", "◎"),
    ("dogecoin", "Ð")
]

def get_currency_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=f"{emoji} {coin.capitalize()}") for coin, emoji in POPULAR_COINS[i:i+2]]
            for i in range(0, len(POPULAR_COINS), 2)
        ],
        resize_keyboard=True
    ) 