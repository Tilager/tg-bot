from sqlalchemy import Column, BigInteger, String, sql, Integer

from utils.db_api.db_gino import TimedBaseModel


class UserModel(TimedBaseModel):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger(), unique=True)
    username = Column(String(50), unique=True)
    password = Column(String(200))
    role = Column(String(60))

    query: sql.Select
