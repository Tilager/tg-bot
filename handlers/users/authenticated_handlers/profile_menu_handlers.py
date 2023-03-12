import datetime

from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboards.default import start_keyboards
from keyboards.inline.authenticated_keyboards import applicant_kb, employer_kb
from keyboards.inline.callback_datas import profile_cb

from loader import dp, bot
from models import UserModel, EmployerModel, ApplicantModel

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
    user: UserModel = await us_ser.get_by_telegram_id(msg.from_user.id)
    match user.role:
        case "Employer":
            employer: EmployerModel = await em_ser.get_employer_by_user_id(user.id)
            text = await get_employer_profile_text(employer)
            await msg.answer(
                text,
                reply_markup=employer_kb.edit_profile_kb
            )

        case "Applicant":
            applicant: ApplicantModel = await ap_ser.get_applicant_by_user_id(user.id)
            text = await get_applicant_profile_text(applicant)
            await msg.answer(
                text,
                reply_markup=applicant_kb.edit_profile_kb
            )


@dp.callback_query_handler(profile_cb.filter())
async def edit_profile(callback: types.CallbackQuery, callback_data: dict, state: FSMContext):
    await state.update_data(chat_id=callback.message.chat.id, message_id=callback.message.message_id)
    match callback_data.get("attribute"):
        case "FCs":
            await callback.answer()
            await callback.message.answer("Введите новое ФИО.")
            await state.set_state("profile:FCs")

        case "birth":
            await callback.answer()
            await callback.message.answer("Введите новую дату рождения.")
            await state.set_state("profile:birth")

        case "phone":
            await callback.answer()
            await callback.message.answer("Введите новый номер телефона.")
            await state.set_state("profile:phone")

        case "passport":
            await callback.answer()
            await callback.message.answer("Введите новые паспортные данные.")
            await state.set_state("profile:passport")

        case "organization":
            await callback.answer()
            await callback.message.answer("Введите новое название организации.")
            await state.set_state("profile:organization")

        case "education":
            await callback.answer()
            await callback.message.answer("Введите ваше образование.")
            await state.set_state("profile:education")

        case "drive_license":
            await callback.answer()
            await callback.message.answer("У вас есть водительские права? (Да, Нет)")
            await state.set_state("profile:drive_license")

        case "military_ticket":
            await callback.answer()
            await callback.message.answer("У вас есть военный билет? (Да, Нет)")
            await state.set_state("profile:military_ticket")

        case "english":
            await callback.answer()
            await callback.message.answer("Вы знаете английский язык? (Да, Нет)")
            await state.set_state("profile:english")


@dp.message_handler(state="profile:FCs")
async def profile_edit_FCs(msg: types.Message, state: FSMContext):
    if not fullmatch(r"^[А-ЯA-Z][а-яА-Яa-zA-Z]+ [А-ЯA-Z][а-яА-Яa-zA-Z]+ [А-ЯA-Z][а-яА-Яa-zA-Z]+$", msg.text):
        await msg.answer("Введите ФИО формата (Иванов Иван Иванов)")
        await state.set_state("profile:FCs")
        return
    else:
        user: UserModel = await us_ser.get_by_telegram_id(msg.from_user.id)
        user_after_update = None

        match user.role:
            case "Employer":
                user_after_update = await em_ser.update_FCs(user.id, msg.text.strip().split())

            case "Applicant":
                user_after_update = await ap_ser.update_FCs(user.id, msg.text.strip().split())

        data = await state.get_data()
        await edit_profile_text(message_id=data.get("message_id"), chat_id=data.get("chat_id"),
                                role=user.role, user=user_after_update)
        await msg.answer("ФИО успешно обновлено!")
        await state.finish()


@dp.message_handler(state="profile:birth")
async def profile_edit_birth(msg: types.Message, state: FSMContext):
    try:
        today = datetime.date.today()
        birth = datetime.datetime.strptime(msg.text.strip(), "%d.%m.%Y").date()
        age = today.year - birth.year - ((today.month, today.day) < (birth.month, birth.day))
        if age > 18:
            user: UserModel = await us_ser.get_by_telegram_id(msg.from_user.id)
            user_after_update = None

            match user.role:
                case "Employer":
                    user_after_update = await em_ser.update_birth(user.id, birth)

                case "Applicant":
                    user_after_update = await ap_ser.update_birth(user.id, birth)

            data = await state.get_data()
            await edit_profile_text(message_id=data.get("message_id"), chat_id=data.get("chat_id"),
                                    role=user.role, user=user_after_update)
            await msg.answer("Дата успешно обновлена!")
            await state.finish()
        else:
            await msg.answer("Вам должно быть больше 18 лет!")
            await state.finish()

    except ValueError:
        await msg.answer("Введите дату рождения формата: 25.11.2000")
        await state.set_state("profile:birth")


@dp.message_handler(state="profile:phone")
async def profile_edit_phone(msg: types.Message, state: FSMContext):
    phone = msg.text.strip()
    if fullmatch(r"^((\+7|7|8)+([0-9]){10})$", phone):
        user: UserModel = await us_ser.get_by_telegram_id(msg.from_user.id)
        user_after_update = None

        match user.role:
            case "Employer":
                user_after_update = await em_ser.update_phone(user.id, phone)

            case "Applicant":
                user_after_update = await ap_ser.update_phone(user.id, phone)

        data = await state.get_data()
        await edit_profile_text(message_id=data.get("message_id"), chat_id=data.get("chat_id"),
                                role=user.role, user=user_after_update)
        await msg.answer("Номер телефона был успешно обновлен!")
        await state.finish()
    else:
        await msg.answer("Номер телефона должен быть формата: +79388640401")
        await state.set_state("profile:phone")


@dp.message_handler(state="profile:organization")
async def profile_edit_passport(msg: types.Message, state: FSMContext):
    user: UserModel = await us_ser.get_by_telegram_id(msg.from_user.id)

    user_after_update = await em_ser.update_organization(user.id, msg.text.strip())

    data = await state.get_data()
    await edit_profile_text(message_id=data.get("message_id"), chat_id=data.get("chat_id"),
                            role=user.role, user=user_after_update)
    await msg.answer("Название организации было успешно обновлено!")
    await state.finish()


@dp.message_handler(state="profile:passport")
async def profile_edit_passport(msg: types.Message, state: FSMContext):
    passport = msg.text.strip()
    if fullmatch(r"\d{4} \d{6}", passport):
        user: UserModel = await us_ser.get_by_telegram_id(msg.from_user.id)
        user_after_update = await em_ser.update_passport(user.id, passport)

        data = await state.get_data()
        await edit_profile_text(message_id=data.get("message_id"), chat_id=data.get("chat_id"),
                                role=user.role, user=user_after_update)
        await msg.answer("Паспортные данные были успешно обновлены!")
        await state.finish()
    else:
        await msg.answer("Введите паспорт формата (9011 567894).")
        await state.set_state("profile:passport")


@dp.message_handler(state="profile:education")
async def profile_edit_education(msg: types.Message, state: FSMContext):
    user: UserModel = await us_ser.get_by_telegram_id(msg.from_user.id)
    user_after_update = await ap_ser.update_education(user.id, msg.text)

    data = await state.get_data()
    await edit_profile_text(message_id=data.get("message_id"), chat_id=data.get("chat_id"),
                            role=user.role, user=user_after_update)
    await msg.answer("Образование было успешно обновлено!")
    await state.finish()


@dp.message_handler(state="profile:drive_license")
async def profile_edit_drive_license(msg: types.Message, state: FSMContext):
    user: UserModel = await us_ser.get_by_telegram_id(msg.from_user.id)
    match msg.text.lower():
        case "да":
            user_after_update = await ap_ser.update_drive_license(user.id, True)
            await state.finish()
        case "нет":
            user_after_update = await ap_ser.update_drive_license(user.id, False)
            await state.finish()
        case _:
            await msg.answer("Ответ может быть только да или нет!. Введите заново.")
            await state.set_state("profile:drive_license")
            return

    data = await state.get_data()
    await edit_profile_text(message_id=data.get("message_id"), chat_id=data.get("chat_id"),
                            role=user.role, user=user_after_update)
    await msg.answer("Данные о водительских правах были обновлены.")
    await state.finish()


@dp.message_handler(state="profile:military_ticket")
async def profile_edit_military_ticket(msg: types.Message, state: FSMContext):
    user: UserModel = await us_ser.get_by_telegram_id(msg.from_user.id)
    match msg.text.lower():
        case "да":
            user_after_update = await ap_ser.update_military_ticket(user.id, True)
            await state.finish()
        case "нет":
            user_after_update = await ap_ser.update_military_ticket(user.id, False)
            await state.finish()
        case _:
            await msg.answer("Ответ может быть только да или нет!. Введите заново.")
            await state.set_state("profile:military_ticket")
            return

    data = await state.get_data()
    await edit_profile_text(message_id=data.get("message_id"), chat_id=data.get("chat_id"),
                            role=user.role, user=user_after_update)
    await msg.answer("Данные о военном билете были обновлены.")
    await state.finish()


@dp.message_handler(state="profile:english")
async def profile_edit_english(msg: types.Message, state: FSMContext):
    user: UserModel = await us_ser.get_by_telegram_id(msg.from_user.id)
    match msg.text.lower():
        case "да":
            user_after_update = await ap_ser.update_english(user.id, True)
            await state.finish()
        case "нет":
            user_after_update = await ap_ser.update_english(user.id, False)
            await state.finish()
        case _:
            await msg.answer("Ответ может быть только да или нет!. Введите заново.")
            await state.set_state("profile:english")
            return

    data = await state.get_data()
    await edit_profile_text(message_id=data.get("message_id"), chat_id=data.get("chat_id"),
                            role=user.role, user=user_after_update)
    await msg.answer("Данные о знание английского были обновлены.")
    await state.finish()


async def get_employer_profile_text(employer: EmployerModel):
    return f"ФИО - {employer.surname} {employer.name} {employer.patronymic}\n" \
           f"Дата рождения - {employer.date_of_birthday.strftime('%d.%m.%Y')}\n" \
           f"Номер телефона - {employer.phone}\n" \
           f"Паспорт - {employer.passport[0:2]}** {employer.passport[5:7]}****\n" \
           f"Название организации - {employer.organization_name}\n"


async def get_applicant_profile_text(applicant: ApplicantModel):
    return f"ФИО - {applicant.surname} {applicant.name} {applicant.patronymic}\n" \
           f"Дата рождения - {applicant.date_of_birthday.strftime('%d.%m.%Y')}\n" \
           f"Номер телефона - {applicant.phone}\n" \
           f"Образование - {applicant.education}\n" \
           f"Водительские права - {'Есть' if applicant.drive_license else 'Нет'}\n" \
           f"Военные билет - {'Есть' if applicant.military_ticket else 'Нет'}\n" \
           f"Знание английского - {'Есть' if applicant.drive_license else 'Нет'}\n"


async def edit_profile_text(message_id: int, chat_id: int, user,
                            role: str):
    match role:
        case "Employer":
            text = await get_employer_profile_text(user)
            await bot.edit_message_text(text=text,
                                        chat_id=chat_id,
                                        message_id=message_id,
                                        reply_markup=employer_kb.edit_profile_kb)

        case "Applicant":
            text = await get_applicant_profile_text(user)
            await bot.edit_message_text(text=text,
                                        chat_id=chat_id,
                                        message_id=message_id,
                                        reply_markup=applicant_kb.edit_profile_kb)
