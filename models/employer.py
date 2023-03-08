from sqlalchemy import Column, Integer, sql, String, ForeignKey, Date

from utils.db_api.db_gino import TimedBaseModel


class EmployerModel(TimedBaseModel):
    __tablename__ = 'employers'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(ForeignKey("users.id"), unique=True)
    name = Column(String(80))
    surname = Column(String(80))
    patronymic = Column(String(80))
    date_of_birthday = Column(Date())
    phone = Column(String(15))
    passport = Column(String(20))
    organization_name = Column(String(80))

    query: sql.Select