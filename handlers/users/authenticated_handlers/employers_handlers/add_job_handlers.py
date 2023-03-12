from aiogram import types
from aiogram.dispatcher import FSMContext

from filters import IsEmployer
from loader import dp
from models import EmployerModel
from states.job_states import Job
from utils.db_api.services import jobs_service as j_ser
from utils.db_api.services import employers_service as em_ser


@dp.message_handler(IsEmployer(), text="Добавить вакансию")
async def add_job(msg: types.Message):
    await msg.answer("Введите должность.")
    await Job.post.set()


@dp.message_handler(state=Job.post)
async def post_enter(msg: types.Message, state: FSMContext):
    await state.update_data(post=msg.text)
    await msg.answer("Введите зар. плату.")
    await Job.salary.set()


@dp.message_handler(state=Job.salary)
async def salary_enter(msg: types.Message, state: FSMContext):
    try:
        salary = float(msg.text)
    except ValueError:
        await msg.answer("Введите зарплату числом!")
        await Job.salary.set()
        return

    await state.update_data(salary=salary)
    await msg.answer("Введите график.")
    await Job.chart.set()


@dp.message_handler(state=Job.chart)
async def chart_enter(msg: types.Message, state: FSMContext):
    await state.update_data(chart=msg.text)
    await msg.answer("Введите количество рабочих часов в неделю.")
    await Job.hours_in_week.set()


@dp.message_handler(state=Job.hours_in_week)
async def hours_enter(msg: types.Message, state: FSMContext):
    try:
        hours = float(msg.text)
    except ValueError:
        await msg.answer("Введите количество числом!")
        await Job.hours_in_week.set()
        return

    await state.update_data(hours_in_week=hours)
    await msg.answer("Требуется ли наличие водительских прав? (Да, Нет)")
    await Job.drive_license.set()


@dp.message_handler(state=Job.drive_license)
async def drive_license_enter(msg: types.Message, state: FSMContext):
    match msg.text.lower():
        case "да":
            await state.update_data(drive_license=True)
        case "нет":
            await state.update_data(drive_license=False)
        case _:
            await msg.answer("Ответ может быть только да или нет!. Введите заново.")
            await Job.drive_license.set()
            return

    await msg.answer("Требуется ли военный билет? (Да, Нет)")
    await Job.military_ticket.set()


@dp.message_handler(state=Job.military_ticket)
async def military_ticket_enter(msg: types.Message, state: FSMContext):
    match msg.text.lower():
        case "да":
            await state.update_data(military_ticket=True)
        case "нет":
            await state.update_data(military_ticket=False)
        case _:
            await msg.answer("Ответ может быть только да или нет!. Введите заново.")
            await Job.military_ticket.set()
            return

    await msg.answer("Требуется ли знание английского языка? (Да, Нет)")
    await Job.english.set()


@dp.message_handler(state=Job.english)
async def english_enter(msg: types.Message, state: FSMContext):
    match msg.text.lower():
        case "да":
            await state.update_data(english=True)
        case "нет":
            await state.update_data(english=False)
        case _:
            await msg.answer("Ответ может быть только да или нет!. Введите заново.")
            await Job.english.set()
            return

    data = await state.get_data()
    employer: EmployerModel = await em_ser.get_employer_by_telegram_id(msg.from_user.id)
    await j_ser.add_job(**data, employer_id=employer.id)
    await msg.answer("Вакансия успешно добавлена!")
    await state.finish()
