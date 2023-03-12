from aiogram.dispatcher.filters.state import StatesGroup, State


class Job(StatesGroup):
    post = State()
    salary = State()
    chart = State()
    hours_in_week = State()
    drive_license = State()
    military_ticket = State()
    english = State()
