import datetime

from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboards.default import start_keyboards
from keyboards.inline import authenticated_menu_kb
from keyboards.inline.callback_datas import profile_cb

from loader import dp
from models import UserModel, EmployerModel

from re import fullmatch

from utils.db_api.services import user_service as us_ser
from utils.db_api.services import employers_service as em_ser
from utils.db_api.services import applicants_service as ap_ser


@dp.message_handler(text="Выйти")
async def logout(msg: types.Message):
    await us_ser.remove_user_id(msg.from_user.id)
    await msg.answer("Вы успешно вышли с аккаунта!", reply_markup=start_keyboards.not_auth_kb)


@dp.message_handler(text="Профиль")
async def get_profile(msg: types.Message):
    user: UserModel = await us_ser.get_by_user_id(msg.from_user.id)
    match user.role:
        case "Employer":
            employer: EmployerModel = await em_ser.get_employer_user_id(user.id)
            text = await get_employer_profile_text(employer)
            await msg.answer(
                text,
                reply_markup=authenticated_menu_kb.edit_profile_employer_kb
            )


@dp.callback_query_handler(profile_cb.filter())
async def edit_profile(callback: types.CallbackQuery, callback_data: dict, state: FSMContext):
    match callback_data.get("attribute"):
        case "FCs":
            await callback.answer()
            await callback.message.answer("Введите новое ФИО.")
            await state.set_state("profile:FCs")
            return

        case "birth":
            await callback.answer()
            await callback.message.answer("Введите новую дату рождения.")
            await state.set_state("profile:birth")
            return

        case "phone":
            await callback.answer()
            await callback.message.answer("Введите новый номер телефона.")
            await state.set_state("profile:phone")
            return

        case "passport":
            await callback.answer()
            await callback.message.answer("Введите новые паспортные данные.")
            await state.set_state("profile:passport")
            return

        case "organization":
            await callback.answer()
            await callback.message.answer("Введите новое название организации.")
            await state.set_state("profile:organization")
            return


@dp.message_handler(state="profile:FCs")
async def profile_edit_FCs(msg: types.Message, state: FSMContext):
    if not fullmatch(r"^[А-ЯA-Z][а-яА-Яa-zA-Z]+ [А-ЯA-Z][а-яА-Яa-zA-Z]+ [А-ЯA-Z][а-яА-Яa-zA-Z]+$", msg.text):
        await msg.answer("Введите ФИО формата (Иванов Иван Иванов)")
        await state.set_state("profile:FCs")
        return
    else:
        user: UserModel = await us_ser.get_by_user_id(msg.from_user.id)
        match user.role:
            case "Employer":
                await em_ser.update_FCs(user.id, msg.text.split())
                await msg.answer("ФИО успешно обновлено!")
                await state.finish()
                return

            case "Applicant":
                await ap_ser.update_FCs(user.id, msg.text.split())
                await msg.answer("ФИО успешно обновлено!")
                await state.finish()
                return


@dp.message_handler(state="profile:birth")
async def profile_edit_FCs(msg: types.Message, state: FSMContext):
    try:
        today = datetime.date.today()
        birth = datetime.datetime.strptime(msg.text, "%d.%m.%Y").date()
        age = today.year - birth.year - ((today.month, today.day) < (birth.month, birth.day))
        if age > 18:
            user: UserModel = await us_ser.get_by_user_id(msg.from_user.id)
            match user.role:
                case "Employer":
                    await em_ser.update_birth(user.id, birth)
                    await msg.answer("Дата успешно обновлена!")
                    await state.finish()
                    return

                case "Applicant":
                    await ap_ser.update_birth(user.id, birth)
                    await msg.answer("Дата успешно обновлена!")
                    await state.finish()
                    return
        else:
            await msg.answer("Вам должно быть больше 18 лет!")
            await state.finish()
            return
    except ValueError:
        await msg.answer("Введите дату рождения формата: 25.11.2000")
        await state.set_state("profile:birth")
        return


async def get_employer_profile_text(employer: EmployerModel):
    return f"ФИО - {employer.surname} {employer.name} {employer.patronymic}\n" \
           f"Дата рождения - {employer.date_of_birthday.strftime('%d.%m.%Y')}\n" \
           f"Номер телефона - {employer.phone}\n" \
           f"Паспорт - {employer.passport[0:2]}** {employer.passport[5:7]}****\n" \
           f"Название организации - {employer.organization_name}\n"
