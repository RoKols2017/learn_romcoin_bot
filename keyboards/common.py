from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

POPULAR_COINS = [
    ("bitcoin", "₿"),
    ("ethereum", "Ξ"),
    ("solana", "◎"),
    ("dogecoin", "Ð")
]

def get_keyboard(command: str) -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=f"/{command} {coin}") for coin, emoji in POPULAR_COINS[i:i+2]]
            for i in range(0, len(POPULAR_COINS), 2)
        ],
        resize_keyboard=True
    ) 