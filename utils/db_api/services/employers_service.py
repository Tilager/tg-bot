import datetime

from asyncpg import UniqueViolationError

from models import EmployerModel, UserModel, JobModel
from utils.db_api.services import user_service as us_ser


async def add_employer(name: str, surname: str, patronymic: str,
                       date_of_birthday: datetime.date, phone: str, passport: str,
                       organization_name: str, username: str, password: str,
                       role: str):
    try:
        user: UserModel = await UserModel.create(username=username, password=password,
                                                 role=role)
        await EmployerModel.create(user_id=user.id, name=name, surname=surname, patronymic=patronymic,
                                   date_of_birthday=date_of_birthday, phone=phone, passport=passport,
                                   organization_name=organization_name)

    except UniqueViolationError:
        raise UniqueViolationError


async def get_employer_by_id(id: int | str):
    employer = await EmployerModel.get(int(id))
    return employer


async def get_employer_by_telegram_id(telegram_id: int):
    user = await us_ser.get_by_telegram_id(telegram_id)
    employer = await EmployerModel.query.where(EmployerModel.user_id == user.id).gino.first()
    return employer


async def get_employer_by_job_id(job_id: int):
    job: JobModel = await JobModel.get(job_id)
    employer: EmployerModel = await EmployerModel.get(job.employer_id)
    return employer


async def get_all_employers():
    employers = await EmployerModel.query.gino.all()
    return employers


async def update_FCs(employer_id: int, FCs: list):
    employer = await EmployerModel.get(int(employer_id))
    surname, name, patronymic = FCs
    await employer.update(name=name, surname=surname, patronymic=patronymic).apply()
    return employer


async def update_birth(employer_id: int, birth: datetime.date):
    employer = await EmployerModel.get(int(employer_id))
    await employer.update(date_of_birthday=birth).apply()
    return employer


async def update_phone(employer_id: int, phone: str):
    employer = await EmployerModel.get(int(employer_id))
    await employer.update(phone=phone).apply()
    return employer


async def update_passport(employer_id: int, passport: str):
    employer = await EmployerModel.get(int(employer_id))
    await employer.update(passport=passport).apply()
    return employer


async def update_organization(employer_id: int, organization: str):
    employer = await EmployerModel.get(int(employer_id))
    await employer.update(organization_name=organization).apply()
    return employer
