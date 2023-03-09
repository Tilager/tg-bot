from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from keyboards.inline import callback_datas

edit_profile_employer_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Изменить ФИО", callback_data=callback_datas.profile_cb.new("FCs")),
     InlineKeyboardButton(text="Изменить дату рождения", callback_data=callback_datas.profile_cb.new("birth"))],
    [InlineKeyboardButton(text="Изменить номер телефона", callback_data=callback_datas.profile_cb.new("phone"))],
    [InlineKeyboardButton(text="Изменить паспорт", callback_data=callback_datas.profile_cb.new("passport")),
     InlineKeyboardButton(text="Изменить название организации",
                          callback_data=callback_datas.profile_cb.new("organization"))]
])