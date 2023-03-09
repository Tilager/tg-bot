import datetime

from asyncpg import UniqueViolationError

from models import EmployerModel, UserModel


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


async def get_employer_user_id(id: int):
    user = await EmployerModel.query.where(EmployerModel.user_id == id).gino.first()
    return user


async def update_FCs(id: int, FCs: list):
    user = await EmployerModel.get(id)
    surname, name, patronymic = FCs
    await user.update(name=name, surname=surname, patronymic=patronymic).apply()


async def update_birth(id: int, birth: datetime.date):
    user = await EmployerModel.get(id)
    await user.update(date_of_birthday=birth).apply()
