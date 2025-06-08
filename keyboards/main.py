from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def get_main_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="/price bitcoin"), KeyboardButton(text="/daily bitcoin")],
            [KeyboardButton(text="/analyze bitcoin"), KeyboardButton(text="/alerts bitcoin")]
        ],
        resize_keyboard=True
    )

def get_start_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="/start"), KeyboardButton(text="/help")]
        ],
        resize_keyboard=True
    ) 