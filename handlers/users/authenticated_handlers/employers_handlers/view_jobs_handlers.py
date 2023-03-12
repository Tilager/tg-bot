from typing import List

from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboards.inline import callback_datas
from keyboards.inline.authenticated_keyboards import employer_kb
from loader import dp, bot
from models import JobModel, EmployerModel
from utils.db_api.services import jobs_service as j_ser
from utils.db_api.services import employers_service as em_ser


@dp.message_handler(text="Просмотреть мои вакансии")
async def view_jobs(msg: types.Message):
    employer: EmployerModel = await em_ser.get_employer_by_telegram_id(msg.from_user.id)
    jobs: List[JobModel] = await j_ser.get_all_jobs_by_employer(employer.id)
    if len(jobs) == 0:
        await msg.answer("У вас нет вакансий!")
    else:
        for job in jobs:
            text = await get_jobs_text(job)
            kb = await employer_kb.create_edit_job_kb(job.id)
            await msg.answer(text=text, reply_markup=kb)


@dp.callback_query_handler(callback_datas.job_cb.filter())
async def view_all_jobs(callback: types.CallbackQuery, callback_data: dict, state: FSMContext):
    await state.update_data(job_id=int(callback_data.get("job_id")),
                            message_id=callback.message.message_id,
                            chat_id=callback.message.chat.id)
    match callback_data.get("attribute"):
        case "post":
            await callback.message.answer("Введите новую должность.")
            await state.set_state("job:post")

        case "salary":
            await callback.message.answer("Введите новую зарплату.")
            await state.set_state("job:salary")

        case "chart":
            await callback.message.answer("Введите новый рабочий график.")
            await state.set_state("job:chart")

        case "hours":
            await callback.message.answer("Введите количество рабочих часов в неделю.")
            await state.set_state("job:hours")

        case "drive_license":
            await callback.message.answer("Требуется ли наличие водительские прав? (Да, Нет)")
            await state.set_state("job:drive_license")

        case "military_ticket":
            await callback.message.answer("Требуется ли наличие военного билета? (Да, Нет)")
            await state.set_state("job:military_ticket")

        case "english":
            await callback.message.answer("Требуется ли наличие английского? (Да, Нет)")
            await state.set_state("job:english")

        case "delete":
            await j_ser.delete_job(int(callback_data.get("job_id")))
            await callback.message.answer("Вакансия успешно удалена!")
            await callback.message.delete()

    await callback.answer()


@dp.message_handler(state="job:post")
async def job_edit_post(msg: types.Message, state: FSMContext):
    data = await state.get_data()
    job: JobModel = await j_ser.update_post(data.get("job_id"), msg.text)
    await edit_job_message(message_id=data.get("message_id"),
                           chat_id=data.get("chat_id"), job=job)

    await msg.answer("Должность успешно обновлена.")
    await state.finish()


@dp.message_handler(state="job:salary")
async def job_edit_salary(msg: types.Message, state: FSMContext):
    data = await state.get_data()

    try:
        salary = float(msg.text)
    except ValueError:
        await msg.answer("Введите зарплату числом!")
        await state.set_state("job:salary")
        return

    job: JobModel = await j_ser.update_salary(data.get("job_id"), salary)
    await edit_job_message(message_id=data.get("message_id"),
                           chat_id=data.get("chat_id"), job=job)
    await msg.answer("Зарплата успешно обновлена.")
    await state.finish()


@dp.message_handler(state="job:chart")
async def job_edit_chart(msg: types.Message, state: FSMContext):
    data = await state.get_data()
    job: JobModel = await j_ser.update_chart(data.get("job_id"), msg.text)
    await edit_job_message(message_id=data.get("message_id"),
                           chat_id=data.get("chat_id"), job=job)

    await msg.answer("График успешно обновлен.")
    await state.finish()


@dp.message_handler(state="job:hours")
async def job_edit_hours(msg: types.Message, state: FSMContext):
    data = await state.get_data()

    try:
        hours = float(msg.text)
    except ValueError:
        await msg.answer("Введите количество часов числом!")
        await state.set_state("job:hours")
        return

    job: JobModel = await j_ser.update_hours_in_week(data.get("job_id"), hours)
    await edit_job_message(message_id=data.get("message_id"),
                           chat_id=data.get("chat_id"), job=job)

    await msg.answer("Количество рабочих часов успешно обновлены.")
    await state.finish()


@dp.message_handler(state="job:drive_license")
async def job_edit_drive_license(msg: types.Message, state: FSMContext):
    data = await state.get_data()

    match msg.text.lower():
        case "да":
            drive_license = True
        case "нет":
            drive_license = False
        case _:
            await msg.answer("Ответ может быть только да или нет!. Введите заново.")
            await state.set_state("job:drive_license")
            return

    job: JobModel = await j_ser.update_drive_license(data.get("job_id"), drive_license)
    await edit_job_message(message_id=data.get("message_id"),
                           chat_id=data.get("chat_id"), job=job)

    await msg.answer("Количество рабочих часов успешно обновлены.")
    await state.finish()


@dp.message_handler(state="job:military_ticket")
async def job_edit_military_ticket(msg: types.Message, state: FSMContext):
    data = await state.get_data()

    match msg.text.lower():
        case "да":
            military_ticket = True
        case "нет":
            military_ticket = False
        case _:
            await msg.answer("Ответ может быть только да или нет!. Введите заново.")
            await state.set_state("job:military_ticket")
            return

    job: JobModel = await j_ser.update_military_ticket(data.get("job_id"), military_ticket)
    await edit_job_message(message_id=data.get("message_id"),
                           chat_id=data.get("chat_id"), job=job)

    await msg.answer("Количество рабочих часов успешно обновлены.")
    await state.finish()


@dp.message_handler(state="job:english")
async def job_edit_english(msg: types.Message, state: FSMContext):
    data = await state.get_data()

    match msg.text.lower():
        case "да":
            english = True
        case "нет":
            english = False
        case _:
            await msg.answer("Ответ может быть только да или нет!. Введите заново.")
            await state.set_state("job:english")
            return

    job: JobModel = await j_ser.update_english(data.get("job_id"), english)
    await edit_job_message(message_id=data.get("message_id"),
                           chat_id=data.get("chat_id"), job=job)

    await msg.answer("Количество рабочих часов успешно обновлены.")
    await state.finish()


async def get_jobs_text(job: JobModel):
    return f"Должность - {job.post}\n" \
           f"Зарплата - {job.salary}\n" \
           f"График - {job.chart}\n" \
           f"Количество рабочих часов в неделю - {job.hours_in_week}\n" \
           f"Наличие водительских прав - {'Требуется' if job.drive_license else 'Не требуется'}\n" \
           f"Наличие военного билета - {'Требуется' if job.military_ticket else 'Не требуется'}\n" \
           f"Знание английского - {'Требуется' if job.english else 'Не требуется'}\n"


async def edit_job_message(message_id: int, chat_id: int, job: JobModel):
    kb = await employer_kb.create_edit_job_kb(job.id)
    text = await get_jobs_text(job)
    await bot.edit_message_text(text=text,
                                chat_id=chat_id,
                                message_id=message_id,
                                reply_markup=kb)
