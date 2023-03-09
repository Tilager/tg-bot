from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardRemove

from keyboards.default import start_keyboards
from loader import dp

from utils.db_api.services import user_service as us_ser


@dp.message_handler(text="Войти")
async def authorization(msg: types.Message, state: FSMContext):
    await msg.answer("Введите ваш логин.")
    await state.set_state("auth_username")


@dp.message_handler(state="auth_username")
async def username_enter(msg: types.Message, state: FSMContext):
    await state.update_data(username=msg.text)

    await msg.answer("Введите ваш пароль.")
    await state.set_state("auth_password")


@dp.message_handler(state="auth_password")
async def password_enter(msg: types.Message, state: FSMContext):
    await state.update_data(password=msg.text)
    data = await state.get_data()
    user = await us_ser.select_username_password(**data)
    if user is None:
        await msg.answer("Пользователя с таким логином и паролем не существует!")
    else:
        await us_ser.update_user_id(user.id, msg.from_user.id)

        await msg.answer("Вы успешно вошли.", reply_markup=start_keyboards.auth_kb)

    await state.finish()
