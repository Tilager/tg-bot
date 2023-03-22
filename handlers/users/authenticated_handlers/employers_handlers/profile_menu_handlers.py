import datetime
from re import fullmatch

from aiogram import types
from aiogram.dispatcher import FSMContext

from filters import IsEmployer
from filters.role_filters import IsAdmin
from keyboards.inline.authenticated_keyboards import employer_kb
from loader import dp, bot
from models import EmployerModel
from utils.db_api.services import employers_service as em_ser


@dp.message_handler(IsEmployer(), text="Профиль")
async def get_profile(msg: types.Message):
    employer: EmployerModel = await em_ser.get_employer_by_telegram_id(msg.chat.id)
    text = await get_employer_profile_text(employer)
    kb = await employer_kb.create_edit_profile_kb(employer.id)
    await msg.answer(
        text,
        reply_markup=kb
    )


@dp.message_handler(state="profile:employer:FCs")
async def profile_edit_FCs(msg: types.Message, state: FSMContext):
    if not fullmatch(r"^[А-ЯA-Z][а-яА-Яa-zA-Z]+ [А-ЯA-Z][а-яА-Яa-zA-Z]+ [А-ЯA-Z][а-яА-Яa-zA-Z]+$", msg.text):
        await msg.answer("Введите ФИО формата (Иванов Иван Иванов)")
        await state.set_state("profile:FCs")
        return
    else:
        data = await state.get_data()
        employer_after_update = await em_ser.update_FCs(data.get("profile_id"), msg.text.strip().split())

        await edit_profile_text(message_id=data.get("message_id"), chat_id=data.get("chat_id"),
                                employer=employer_after_update)
        await msg.answer("ФИО успешно обновлено!")
        await state.finish()


@dp.message_handler(state="profile:employer:birth")
async def profile_edit_birth(msg: types.Message, state: FSMContext):
    try:
        today = datetime.date.today()
        birth = datetime.datetime.strptime(msg.text.strip(), "%d.%m.%Y").date()
        age = today.year - birth.year - ((today.month, today.day) < (birth.month, birth.day))
        if age >= 18:
            data = await state.get_data()
            employer_after_update = await em_ser.update_birth(data.get("profile_id"), birth)

            await edit_profile_text(message_id=data.get("message_id"), chat_id=data.get("chat_id"),
                                    employer=employer_after_update)
            await msg.answer("Дата успешно обновлена!")
            await state.finish()
        else:
            await msg.answer("Вам должно быть больше 18 лет!")
            await state.finish()

    except ValueError:
        await msg.answer("Введите дату рождения формата: 25.11.2000")
        await state.set_state("profile:employer:birth")


@dp.message_handler(state="profile:employer:phone")
async def profile_edit_phone(msg: types.Message, state: FSMContext):
    phone = msg.text.strip()
    if fullmatch(r"^((\+7|7|8)+([0-9]){10})$", phone):
        data = await state.get_data()
        employer_after_update = await em_ser.update_phone(data.get("profile_id"), phone)

        await edit_profile_text(message_id=data.get("message_id"), chat_id=data.get("chat_id"),
                                employer=employer_after_update)
        await msg.answer("Номер телефона был успешно обновлен!")
        await state.finish()
    else:
        await msg.answer("Номер телефона должен быть формата: +79388640401")
        await state.set_state("profile:phone")


@dp.message_handler(state="profile:employer:organization")
async def profile_edit_passport(msg: types.Message, state: FSMContext):
    data = await state.get_data()
    employer_after_update = await em_ser.update_organization(data.get("profile_id"), msg.text.strip())

    await edit_profile_text(message_id=data.get("message_id"), chat_id=data.get("chat_id"),
                            employer=employer_after_update)
    await msg.answer("Название организации было успешно обновлено!")
    await state.finish()


@dp.message_handler(state="profile:employer:passport")
async def profile_edit_passport(msg: types.Message, state: FSMContext):
    passport = msg.text.strip()
    if fullmatch(r"\d{4} \d{6}", passport):
        data = await state.get_data()
        employer_after_update = await em_ser.update_passport(data.get("profile_id"), passport)

        await edit_profile_text(message_id=data.get("message_id"), chat_id=data.get("chat_id"),
                                employer=employer_after_update)
        await msg.answer("Паспортные данные были успешно обновлены!")
        await state.finish()
    else:
        await msg.answer("Введите паспорт формата (9011 567894).")
        await state.set_state("profile:passport")


async def get_employer_profile_text(employer: EmployerModel):
    return f"ФИО - {employer.surname} {employer.name} {employer.patronymic}\n" \
           f"Дата рождения - {employer.date_of_birthday.strftime('%d.%m.%Y')}\n" \
           f"Номер телефона - {employer.phone}\n" \
           f"Паспорт - {employer.passport[0:2]}** {employer.passport[5:7]}****\n" \
           f"Название организации - {employer.organization_name}\n"


async def edit_profile_text(message_id: int, chat_id: int, employer: EmployerModel):
    kb = await employer_kb.create_edit_profile_kb(employer.id)
    text = await get_employer_profile_text(employer)
    await bot.edit_message_text(text=text,
                                chat_id=chat_id,
                                message_id=message_id,
                                reply_markup=kb)
