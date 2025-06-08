from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def get_help_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="/price"), KeyboardButton(text="/daily")],
            [KeyboardButton(text="/analyze"), KeyboardButton(text="/alerts")]
        ],
        resize_keyboard=True
    ) 