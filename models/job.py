from sqlalchemy import Column, String, Float, Boolean, Integer, ForeignKey
from sqlalchemy.sql import Select

from utils.db_api.db_gino import TimedBaseModel


class JobModel(TimedBaseModel):
    __tablename__ = 'jobs'

    id = Column(Integer, primary_key=True, autoincrement=True)
    employer_id = Column(ForeignKey("employers.id"))
    post = Column(String(200))
    salary = Column(Float())
    chart = Column(String(80))
    hours_in_week = Column(Float())
    drive_license = Column(Boolean())
    military_ticket = Column(Boolean())
    english = Column(Boolean())

    query: Select
