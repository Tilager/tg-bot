from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

not_auth_kb = ReplyKeyboardMarkup([
    [KeyboardButton(text="Войти"), KeyboardButton(text="Зарегистрироваться")]
], resize_keyboard=True, one_time_keyboard=False)

auth_employer_kb = ReplyKeyboardMarkup([
    [KeyboardButton(text="Профиль"), KeyboardButton(text="Добавить вакансию")],
    [KeyboardButton(text="Просмотреть мои вакансии")],
    [KeyboardButton(text="Выйти")]
], resize_keyboard=True, one_time_keyboard=False)

auth_applicant_kb = ReplyKeyboardMarkup([
    [KeyboardButton(text="Профиль"), KeyboardButton(text="Просмотреть вакансии")],
    [KeyboardButton(text="Выйти")]
], resize_keyboard=True, one_time_keyboard=False)
