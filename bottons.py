from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


kanal=InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Kanalga azo bo'lish", callback_data="azolik")]
    ]
)


Menyu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Telefon raqamimni yuborish 📞", request_contact=True)]
    ],
    resize_keyboard=True, one_time_keyboard=True
)

