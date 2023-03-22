from typing import List

from aiogram import types
from aiogram.types import CallbackQuery

from filters import IsApplicant
from keyboards.inline import callback_datas
from keyboards.inline.authenticated_keyboards import applicant_kb
from loader import dp
from models import JobModel, EmployerModel
from utils.db_api.services import jobs_service as j_ser
from utils.db_api.services import employers_service as em_ser


@dp.message_handler(IsApplicant(), text="Просмотреть вакансии")
async def view_all_jobs(msg: types.Message):
    jobs: List[JobModel] = await j_ser.get_all_jobs()
    if len(jobs) == 0:
        await msg.answer("На данный момент нет вакансий!")
    else:
        for job in jobs:
            text = await get_job_text(job)
            kb = await applicant_kb.create_edit_job_kb(job.id)
            await msg.answer(text=text, reply_markup=kb)


@dp.callback_query_handler(IsApplicant(), callback_datas.view_job_cb.filter())
async def get_employer_info(callback: CallbackQuery, callback_data: dict):
    employer: EmployerModel = await em_ser.get_employer_by_job_id(int(callback_data.get("job_id")))
    alert_text = await get_alert_text(employer)
    await callback.answer(alert_text, show_alert=True)


async def get_job_text(job: JobModel) -> str:
    return f"Должность - {job.post}\n" \
           f"Зарплата - {job.salary}\n" \
           f"График - {job.chart}\n" \
           f"Количество рабочих часов в неделю - {job.hours_in_week}\n" \
           f"Наличие водительских прав - {'Требуется' if job.drive_license else 'Не требуется'}\n" \
           f"Наличие военного билета - {'Требуется' if job.military_ticket else 'Не требуется'}\n" \
           f"Знание английского - {'Требуется' if job.english else 'Не требуется'}\n"


async def get_alert_text(employer: EmployerModel):
    return f"ФИО - {employer.surname} {employer.name} {employer.patronymic}\n" \
           f"Номер телефона - {employer.phone}\n" \
           f"Название организации - {employer.organization_name}"
