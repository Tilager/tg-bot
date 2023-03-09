from aiogram.dispatcher.filters.state import StatesGroup, State


class User(StatesGroup):
    username = State()
    password = State()
    name = State()
    surname = State()
    patronymic = State()
    date_of_birthday = State()
    phone = State()


class Applicant(User):
    education = State()
    drive_license = State()
    military_ticket = State()
    english = State()


class Employer(User):
    passport = State()
    organization_name = State()