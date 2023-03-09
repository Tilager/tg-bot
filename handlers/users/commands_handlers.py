from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command, CommandStart, CommandHelp

from keyboards.default import start_keyboards
from loader import dp

from utils.db_api.services import user_service as us_ser


@dp.message_handler(CommandHelp())
async def bot_help(message: types.Message):
    text = ("Список команд: ",
            "/start - Начать диалог",
            "/help - Получить справку")

    await message.answer("\n".join(text))


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    user = await us_ser.get_by_user_id(message.from_user.id)
    authenticated: bool = user is not None
    await message.answer(
        f"Здравствуйте, вас приветствует кадровое агенство 'Obair Aisling'.",
        reply_markup=start_keyboards.not_auth_kb if not authenticated else start_keyboards.auth_kb)


@dp.message_handler(Command("cancel"), state="*")
async def state_cancel(msg: types.Message, state: FSMContext):
    await msg.answer("Действие отменено!")
    await state.finish()
