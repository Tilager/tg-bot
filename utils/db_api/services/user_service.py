from asyncpg import UniqueViolationError

from models import UserModel


async def add_user(username: str, password: str, role: str):
    try:
        user = UserModel(username=username, password=password, role=role)

        await user.create()

    except UniqueViolationError:
        pass


async def select_all_users():
    users = await UserModel.query.gino.all()
    return users


async def select_username_password(username: str, password: str) -> UserModel:
    user = await UserModel.query.where((UserModel.username == username) &
                                       (UserModel.password == password)).gino.first()
    return user


async def get_by_telegram_id(user_id: int) -> UserModel:
    user = await UserModel.query.where(UserModel.user_id == user_id).gino.first()
    return user


async def update_user_id(id: int, user_id: int):
    old_user = await get_by_telegram_id(user_id)
    user = await UserModel.get(id)
    if (old_user is not None) and old_user != user:
        await old_user.update(user_id=None).apply()

    await user.update(user_id=user_id).apply()


async def remove_user_id(user_id: int):
    user = await get_by_telegram_id(user_id)

    if user is not None:
        await user.update(user_id=None).apply()
