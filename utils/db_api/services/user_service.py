from asyncpg import UniqueViolationError

from models import UserModel


async def addUser(username: str, password: str, role: str):
    try:
        user = UserModel(username=username, password=password, role=role)

        await user.create()

    except UniqueViolationError:
        pass


async def selectAllUsers():
    users = await UserModel.query.gino.all()
    return users


async def selectUser(id: int):
    user = await UserModel.query.where(UserModel.id == id).gino.first()
    return user


async def updateUsername(id: int, username: str):
    user = await UserModel.get(id)
    await user.update(username=username).apply()