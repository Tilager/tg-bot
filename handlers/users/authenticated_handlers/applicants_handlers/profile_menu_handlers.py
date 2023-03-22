import datetime
from re import fullmatch

from aiogram import types
from aiogram.dispatcher import FSMContext

from filters import IsApplicant
from filters.role_filters import IsAdmin
from keyboards.inline.authenticated_keyboards import applicant_kb
from loader import dp, bot
from models import ApplicantModel
from utils.db_api.services import applicants_service as ap_ser


@dp.message_handler(IsApplicant(), text="Профиль")
async def get_profile(msg: types.Message):
    applicant: ApplicantModel = await ap_ser.get_applicant_by_telegram_id(msg.chat.id)
    text = await get_applicant_profile_text(applicant)
    kb = await applicant_kb.create_edit_profile_kb(applicant.id)
    await msg.answer(
        text,
        reply_markup=kb
    )


@dp.message_handler(state="profile:applicant:FCs")
async def profile_edit_FCs(msg: types.Message, state: FSMContext):
    if not fullmatch(r"^[А-ЯA-Z][а-яА-Яa-zA-Z]+ [А-ЯA-Z][а-яА-Яa-zA-Z]+ [А-ЯA-Z][а-яА-Яa-zA-Z]+$", msg.text):
        await msg.answer("Введите ФИО формата (Иванов Иван Иванов)")
        await state.set_state("profile:FCs")
        return
    else:
        data = await state.get_data()
        applicant: ApplicantModel = await ap_ser.get_applicant_by_id(data.get('profile_id'))
        applicant_after_update = await ap_ser.update_FCs(applicant.id, msg.text.strip().split())

        await edit_profile_text(message_id=data.get("message_id"), chat_id=data.get("chat_id"),
                                applicant=applicant_after_update)
        await msg.answer("ФИО успешно обновлено!")
        await state.finish()


@dp.message_handler(state="profile:applicant:birth")
async def profile_edit_birth(msg: types.Message, state: FSMContext):
    try:
        today = datetime.date.today()
        birth = datetime.datetime.strptime(msg.text.strip(), "%d.%m.%Y").date()
        age = today.year - birth.year - ((today.month, today.day) < (birth.month, birth.day))
        if age >= 18:
            data = await state.get_data()
            applicant: ApplicantModel = await ap_ser.get_applicant_by_id(data.get('profile_id'))
            applicant_after_update = await ap_ser.update_birth(applicant.id, birth)

            await edit_profile_text(message_id=data.get("message_id"), chat_id=data.get("chat_id"),
                                    applicant=applicant_after_update)
            await msg.answer("Дата успешно обновлена!")
            await state.finish()
        else:
            await msg.answer("Вам должно быть больше 18 лет!")
            await state.finish()

    except ValueError:
        await msg.answer("Введите дату рождения формата: 25.11.2000")
        await state.set_state("profile:birth")


@dp.message_handler(state="profile:applicant:phone")
async def profile_edit_phone(msg: types.Message, state: FSMContext):
    phone = msg.text.strip()
    if fullmatch(r"^((\+7|7|8)+([0-9]){10})$", phone):
        data = await state.get_data()
        applicant_after_update = await ap_ser.update_phone(data.get('profile_id'), phone)

        await edit_profile_text(message_id=data.get("message_id"), chat_id=data.get("chat_id"),
                                applicant=applicant_after_update)
        await msg.answer("Номер телефона был успешно обновлен!")
        await state.finish()
    else:
        await msg.answer("Номер телефона должен быть формата: +79388640401")
        await state.set_state("profile:phone")


@dp.message_handler(state="profile:applicant:education")
async def profile_edit_education(msg: types.Message, state: FSMContext):
    data = await state.get_data()
    applicant_after_update = await ap_ser.update_education(data.get('profile_id'), msg.text)

    await edit_profile_text(message_id=data.get("message_id"), chat_id=data.get("chat_id"),
                            applicant=applicant_after_update)
    await msg.answer("Образование было успешно обновлено!")
    await state.finish()


@dp.message_handler(state="profile:applicant:drive_license")
async def profile_edit_drive_license(msg: types.Message, state: FSMContext):
    data = await state.get_data()
    match msg.text.lower():
        case "да":
            applicant_after_update = await ap_ser.update_drive_license(data.get('profile_id'), True)
        case "нет":
            applicant_after_update = await ap_ser.update_drive_license(data.get('profile_id'), False)
        case _:
            await msg.answer("Ответ может быть только да или нет!. Введите заново.")
            await state.set_state("profile:drive_license")
            return

    await edit_profile_text(message_id=data.get("message_id"), chat_id=data.get("chat_id"),
                            applicant=applicant_after_update)
    await msg.answer("Данные о водительских правах были обновлены.")
    await state.finish()


@dp.message_handler(state="profile:applicant:military_ticket")
async def profile_edit_military_ticket(msg: types.Message, state: FSMContext):
    data = await state.get_data()
    match msg.text.lower():
        case "да":
            applicant_after_update = await ap_ser.update_military_ticket(data.get('profile_id'), True)
        case "нет":
            applicant_after_update = await ap_ser.update_military_ticket(data.get('profile_id'), False)
        case _:
            await msg.answer("Ответ может быть только да или нет!. Введите заново.")
            await state.set_state("profile:military_ticket")
            return

    await edit_profile_text(message_id=data.get("message_id"), chat_id=data.get("chat_id"),
                            applicant=applicant_after_update)
    await msg.answer("Данные о военном билете были обновлены.")
    await state.finish()


@dp.message_handler(state="profile:applicant:english")
async def profile_edit_english(msg: types.Message, state: FSMContext):
    data = await state.get_data()
    match msg.text.lower():
        case "да":
            applicant_after_update = await ap_ser.update_english(data.get('profile_id'), True)
        case "нет":
            applicant_after_update = await ap_ser.update_english(data.get('profile_id'), False)
        case _:
            await msg.answer("Ответ может быть только да или нет!. Введите заново.")
            await state.set_state("profile:english")
            return

    await edit_profile_text(message_id=data.get("message_id"), chat_id=data.get("chat_id"),
                            applicant=applicant_after_update)
    await msg.answer("Данные о знание английского были обновлены.")
    await state.finish()


async def get_applicant_profile_text(applicant: ApplicantModel):
    return f"ФИО - {applicant.surname} {applicant.name} {applicant.patronymic}\n" \
           f"Дата рождения - {applicant.date_of_birthday.strftime('%d.%m.%Y')}\n" \
           f"Номер телефона - {applicant.phone}\n" \
           f"Образование - {applicant.education}\n" \
           f"Водительские права - {'Есть' if applicant.drive_license else 'Нет'}\n" \
           f"Военные билет - {'Есть' if applicant.military_ticket else 'Нет'}\n" \
           f"Знание английского - {'Есть' if applicant.english else 'Нет'}\n"


async def edit_profile_text(message_id: int, chat_id: int, applicant: ApplicantModel):
    kb = await applicant_kb.create_edit_profile_kb(applicant.id)
    text = await get_applicant_profile_text(applicant)
    await bot.edit_message_text(text=text,
                                chat_id=chat_id,
                                message_id=message_id,
                                reply_markup=kb)
