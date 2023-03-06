from aiogram import types
from aiogram.dispatcher import FSMContext

from loader import dp
from utils.db_api import db


@dp.message_handler(text="Зарегистрироваться")
async def login(msg: types.Message, state: FSMContext):
    await msg.answer(text="Введите ваш логин")
    await state.set_state(state="username")


@dp.message_handler(state="username")
async def username(msg: types.Message, state: FSMContext):
    await state.update_data(username=msg.text)
    await msg.answer("Введите ваш пароль")
    await state.set_state(state="password")


@dp.message_handler(state="password")
async def password(msg: types.Message, state: FSMContext):
    data = await state.get_data()
    db.save_user(data.get("username"), msg.text)
