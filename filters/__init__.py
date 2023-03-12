from aiogram import Dispatcher

from loader import dp
from .role_filters import IsEmployer
from .role_filters import IsApplicant


if __name__ == "filters":
    dp.filters_factory.bind(IsEmployer)
    dp.filters_factory.bind(IsApplicant)
