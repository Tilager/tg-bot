from typing import List

from aiogram import types

from filters.role_filters import IsAdmin
from handlers.users.authenticated_handlers.employers_handlers.profile_menu_handlers import get_employer_profile_text
from keyboards.inline.authenticated_keyboards import employer_kb
from models import EmployerModel
from utils.db_api.services import employers_service as em_ser
from loader import dp


@dp.message_handler(IsAdmin(), text="Просмотреть всех работодателей")
async def view_all_employers(msg: types.Message):
    employers: List[EmployerModel] = await em_ser.get_all_employers()
    for employer in employers:
        text = await get_employer_profile_text(employer)
        kb = await employer_kb.create_edit_profile_kb(employer.id)
        await msg.answer(
            text,
            reply_markup=kb
        )
