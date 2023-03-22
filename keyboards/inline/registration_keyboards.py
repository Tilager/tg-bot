from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

reg_kb = InlineKeyboardMarkup(row_width=2, inline_keyboard=[
    [InlineKeyboardButton(text="Работодатель", callback_data="reg:employer"),
     InlineKeyboardButton(text="Соискатель", callback_data="reg:applicant")]
])

reg_admin_kb = InlineKeyboardMarkup(row_width=2, inline_keyboard=[
    [InlineKeyboardButton(text="Работодатель", callback_data="reg:employer"),
     InlineKeyboardButton(text="Соискатель", callback_data="reg:applicant")],
    [InlineKeyboardButton(text="Администратор", callback_data="reg:admin")]
])