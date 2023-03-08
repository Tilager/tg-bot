from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

kb = ReplyKeyboardMarkup([
    [KeyboardButton(text="Войти"), KeyboardButton(text="Зарегистрироваться")]
], resize_keyboard=True, one_time_keyboard=True)
