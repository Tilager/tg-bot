from typing import List

from aiogram import types

from handlers.users.authenticated_handlers.applicants_handlers.profile_menu_handlers import get_applicant_profile_text
from keyboards.inline.authenticated_keyboards import applicant_kb
from loader import dp
from models import ApplicantModel

from utils.db_api.services import applicants_service as ap_ser


@dp.message_handler(text="Просмотреть всех соискателей")
async def get_all_applicants(msg: types.Message):
    applicants: List[ApplicantModel] = await ap_ser.get_all_applicants()
    for applicant in applicants:
        text = await get_applicant_profile_text(applicant)
        kb = await applicant_kb.create_edit_profile_kb(applicant.id)
        await msg.answer(
            text,
            reply_markup=kb
        )
