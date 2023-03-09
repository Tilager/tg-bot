import datetime

from asyncpg import UniqueViolationError

from models import ApplicantModel, UserModel


async def addApplicant(name: str, surname: str, patronymic: str,
                       date_of_birthday: datetime.date, phone: str, education: str,
                       drive_license: bool, military_ticket: bool, english: bool,
                       username: str, password: str, role: str):
    try:
        user: UserModel = await UserModel.create(username=username, password=password,
                                                 role=role)

        await ApplicantModel.create(user_id=user.id, name=name, surname=surname, patronymic=patronymic,
                                    date_of_birthday=date_of_birthday, phone=phone, education=education,
                                    drive_license=drive_license, military_ticket=military_ticket,
                                    english=english)

    except UniqueViolationError:
        raise UniqueViolationError


async def update_FCs(id: int, FCs: list):
    user = await ApplicantModel.get(id)
    surname, name, patronymic = FCs
    await user.update(name=name, surname=surname, patronymic=patronymic).apply()


async def update_birth(id: int, birth: datetime.date):
    user = await ApplicantModel.get(id)
    await user.update(date_of_birthday=birth).apply()
