from sqlalchemy import Integer, Column, ForeignKey, String, sql, Boolean, Date

from utils.db_api.db_gino import TimedBaseModel


class ApplicantModel(TimedBaseModel):
    __tablename__ = 'applicants'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(ForeignKey("users.id"), unique=True)
    name = Column(String(80))
    surname = Column(String(80))
    patronymic = Column(String(80))
    date_of_birthday = Column(Date())
    phone = Column(String(15))
    education = Column(String(500))
    drive_license = Column(Boolean())
    military_ticket = Column(Boolean())
    english = Column(Boolean())

    query: sql.Select