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


async def get_applicant_by_user_id(user_id: int):
    user = await ApplicantModel.query.where(ApplicantModel.user_id == user_id).gino.first()
    return user


async def update_FCs(user_id: int, FCs: list):
    user = await get_applicant_by_user_id(user_id)
    surname, name, patronymic = FCs
    await user.update(name=name, surname=surname, patronymic=patronymic).apply()
    return user


async def update_birth(user_id: int, birth: datetime.date):
    user = await get_applicant_by_user_id(user_id)
    await user.update(date_of_birthday=birth).apply()
    return user


async def update_phone(user_id: int, phone: str):
    user = await get_applicant_by_user_id(user_id)
    await user.update(phone=phone).apply()
    return user


async def update_education(user_id: int, education: str):
    user = await get_applicant_by_user_id(user_id)
    await user.update(education=education).apply()
    return user


async def update_drive_license(user_id: int, drive_license: bool):
    user = await get_applicant_by_user_id(user_id)
    await user.update(drive_license=drive_license).apply()
    return user


async def update_military_ticket(user_id: int, military_ticket: bool):
    user = await get_applicant_by_user_id(user_id)
    await user.update(military_ticket=military_ticket).apply()
    return user


async def update_english(user_id: int, english: bool):
    user = await get_applicant_by_user_id(user_id)
    await user.update(english=english).apply()
    return user
