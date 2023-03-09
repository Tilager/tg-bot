from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

not_auth_kb = ReplyKeyboardMarkup([
    [KeyboardButton(text="Войти"), KeyboardButton(text="Зарегистрироваться")]
], resize_keyboard=True, one_time_keyboard=True)


auth_kb = ReplyKeyboardMarkup([
    [KeyboardButton(text="Профиль"), KeyboardButton(text="Выйти")]
], resize_keyboard=True, one_time_keyboard=True)