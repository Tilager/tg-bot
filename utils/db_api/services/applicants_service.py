import datetime

from asyncpg import UniqueViolationError

from models import ApplicantModel, UserModel
from utils.db_api.services import user_service as us_ser


async def get_all_applicants():
    applicants = await ApplicantModel.query.gino.all()
    return applicants


async def add_applicant(name: str, surname: str, patronymic: str,
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


async def get_applicant_by_id(id: int | str):
    applicant = await ApplicantModel.get(int(id))
    return applicant


async def get_applicant_by_telegram_id(telegram_id: int):
    user = await us_ser.get_by_telegram_id(telegram_id)
    applicant = await ApplicantModel.query.where(ApplicantModel.user_id == user.id).gino.first()
    return applicant


async def update_FCs(applicant_id: int, FCs: list):
    applicant: ApplicantModel = await ApplicantModel.get(int(applicant_id))
    surname, name, patronymic = FCs
    await applicant.update(name=name, surname=surname, patronymic=patronymic).apply()
    return applicant


async def update_birth(applicant_id: int, birth: datetime.date):
    applicant: ApplicantModel = await ApplicantModel.get(int(applicant_id))
    await applicant.update(date_of_birthday=birth).apply()
    return applicant


async def update_phone(applicant_id: int, phone: str):
    applicant: ApplicantModel = await ApplicantModel.get(int(applicant_id))
    await applicant.update(phone=phone).apply()
    return applicant


async def update_education(applicant_id: int, education: str):
    applicant: ApplicantModel = await ApplicantModel.get(int(applicant_id))
    await applicant.update(education=education).apply()
    return applicant


async def update_drive_license(applicant_id: int, drive_license: bool):
    applicant: ApplicantModel = await ApplicantModel.get(int(applicant_id))
    await applicant.update(drive_license=drive_license).apply()
    return applicant


async def update_military_ticket(applicant_id: int, military_ticket: bool):
    applicant: ApplicantModel = await ApplicantModel.get(int(applicant_id))
    await applicant.update(military_ticket=military_ticket).apply()
    return applicant


async def update_english(applicant_id: int, english: bool):
    applicant: ApplicantModel = await ApplicantModel.get(int(applicant_id))
    await applicant.update(english=english).apply()
    return applicant
