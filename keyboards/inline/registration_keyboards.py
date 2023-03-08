from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

kb = InlineKeyboardMarkup(row_width=2, inline_keyboard=[
    [InlineKeyboardButton(text="Работодатель", callback_data="reg:employer"),
     InlineKeyboardButton(text="Соискатель", callback_data="reg:applicant")]
])