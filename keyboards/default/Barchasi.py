from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

admin_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Kino yuklash"),
        ],
        [
            KeyboardButton(text="//count"),
            KeyboardButton(text="//reklama")
        ],
    ], resize_keyboard=True
)

admin_only = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="/admin"),
        ],
    ], resize_keyboard=True
)