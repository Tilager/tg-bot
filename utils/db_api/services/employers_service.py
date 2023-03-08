import datetime

from asyncpg import UniqueViolationError

from models import EmployerModel, UserModel


async def addEmployer(name: str, surname: str, patronymic: str,
                      date_of_birthday: datetime.date, phone: str, passport: str,
                      organization_name: str, username: str, password: str):
    try:
        user: UserModel = await UserModel.create(username=username, password=password)
        await EmployerModel.create(user_id=user.id, name=name, surname=surname, patronymic=patronymic,
                                   date_of_birthday=date_of_birthday, phone=phone, passport=passport,
                                   organization_name=organization_name)

    except UniqueViolationError:
        raise UniqueViolationError
