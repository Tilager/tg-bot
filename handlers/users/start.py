from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart

from keyboards.default import startKeyboards
from loader import dp


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    await message.answer(f"Здравствуйте, это кадровое агенство 'Obair Aisling'. Выберите действие, которое вы хотите выполнить",
                         reply_markup=startKeyboards.kb)
