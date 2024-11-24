from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

obuna_inline = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Channel 1",  url="https://t.me/krinjlarr"),
        ],
        [
            InlineKeyboardButton(text="Channel 2",  url="https://t.me/hamitjanof_official"),
        ],
        [
            InlineKeyboardButton(text="Channel 3",  url="https://t.me/azoblash_xizmati"),
        ],
        [
            InlineKeyboardButton(text="✅Tasdiklash", callback_data='tasdiklash')
        ],
    ]
)