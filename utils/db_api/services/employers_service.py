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


async def get_employer_by_user_id(user_id: int):
    user = await EmployerModel.query.where(EmployerModel.user_id == user_id).gino.first()
    return user


async def get_employer_by_telegram_id(telegram_id: int):
    user = await us_ser.get_by_telegram_id(telegram_id)
    employer = await EmployerModel.query.where(EmployerModel.user_id == user.id).gino.first()
    return employer


async def get_employer_by_job_id(job_id: int):
    job: JobModel = await JobModel.get(job_id)
    employer: EmployerModel = await EmployerModel.get(job.employer_id)
    return employer


async def update_FCs(user_id: int, FCs: list):
    user = await get_employer_by_user_id(user_id)
    surname, name, patronymic = FCs
    await user.update(name=name, surname=surname, patronymic=patronymic).apply()
    return user


async def update_birth(user_id: int, birth: datetime.date):
    user = await get_employer_by_user_id(user_id)
    await user.update(date_of_birthday=birth).apply()
    return user


async def update_phone(user_id: int, phone: str):
    user = await get_employer_by_user_id(user_id)
    await user.update(phone=phone).apply()
    return user


async def update_passport(user_id: int, passport: str):
    user = await get_employer_by_user_id(user_id)
    await user.update(passport=passport).apply()
    return user


async def update_organization(user_id: int, organization: str):
    user = await get_employer_by_user_id(user_id)
    await user.update(organization_name=organization).apply()
    return user
