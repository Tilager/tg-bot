from typing import List

from aiogram import types

from filters.role_filters import IsAdmin
from handlers.users.authenticated_handlers.employers_handlers.view_jobs_handlers import get_jobs_text
from keyboards.inline.authenticated_keyboards import employer_kb
from models import JobModel
from utils.db_api.services import jobs_service as j_ser
from loader import dp


@dp.message_handler(IsAdmin(), text="Просмотреть все вакансии")
async def get_all_jobs(msg: types.Message):
    jobs: List[JobModel] = await j_ser.get_all_jobs()

    if len(jobs) == 0:
        await msg.answer("На данный момент нет вакансий!")
    else:
        for job in jobs:
            text = await get_jobs_text(job)
            kb = await employer_kb.create_edit_job_kb(job.id)
            await msg.answer(text=text, reply_markup=kb)
