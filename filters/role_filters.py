from aiogram import types
from aiogram.dispatcher.filters import BoundFilter
from aiogram.types import CallbackQuery

from data import config
from utils.db_api.services.user_service import get_role_by_telegram_id


class IsEmployer(BoundFilter):
    async def check(self, data: CallbackQuery | types.Message) -> bool:
        if type(data) == types.CallbackQuery:
            id = data.message.chat.id
        elif type(data) == types.Message:
            id = data.chat.id
        else:
            return False

        role: str = await get_role_by_telegram_id(id)
        return role == "Employer"


class IsApplicant(BoundFilter):
    async def check(self, data) -> bool:
        if type(data) == types.CallbackQuery:
            id = data.message.chat.id
        elif type(data) == types.Message:
            id = data.chat.id
        else:
            return False

        role: str = await get_role_by_telegram_id(id)
        return role == "Applicant"


class IsAdmin(BoundFilter):
    async def check(self, data) -> bool:
        if type(data) == types.CallbackQuery:
            id = data.message.chat.id
        elif type(data) == types.Message:
            id = data.chat.id
        else:
            return False

        role: str = await get_role_by_telegram_id(id)
        return role == 'Admin'


class IsNotAuthenticated(BoundFilter):
    async def check(self, data) -> bool:
        if type(data) == types.CallbackQuery:
            id = data.message.chat.id
        elif type(data) == types.Message:
            id = data.chat.id
        else:
            return False

        role: str = await get_role_by_telegram_id(id)
        return role is None
