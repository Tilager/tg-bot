import datetime
from re import fullmatch

from aiogram import types
from aiogram.dispatcher import FSMContext

from asyncpg import UniqueViolationError

from keyboards.inline.registration_keyboards import kb
from loader import dp
from states.registration_states import Employer, User, Applicant
from utils.db_api.services import employers_service as em_ser
from utils.db_api.services import applicants_service as ap_ser


@dp.message_handler(text="Зарегистрироваться")
async def login(msg: types.Message):
    await msg.answer(text="Кем вы являетесь?", reply_markup=kb)


@dp.callback_query_handler(text="reg:employer")
async def register_employer(call: types.CallbackQuery, state: FSMContext):
    await state.update_data(role="Employer")
    await call.answer()
    await call.message.answer("Введите ваше имя.")
    await Employer.name.set()


@dp.callback_query_handler(text="reg:applicant")
async def register_applicant(call: types.CallbackQuery, state: FSMContext):
    await state.update_data(role="Applicant")
    await call.answer()
    await call.message.answer("Введите ваше имя.")
    await Applicant.name.set()


@dp.message_handler(state=User.name)
async def name_enter(msg: types.Message, state: FSMContext):
    await state.update_data(name=msg.text)
    await msg.answer("Введите вашу фамилию.")
    await Employer.surname.set()


@dp.message_handler(state=User.surname)
async def surname_enter(msg: types.Message, state: FSMContext):
    await state.update_data(surname=msg.text)
    await msg.answer("Введите ваше отчество.")
    await Employer.patronymic.set()


@dp.message_handler(state=User.patronymic)
async def patronymic_enter(msg: types.Message, state: FSMContext):
    await state.update_data(patronymic=msg.text)
    await msg.answer("Введите вашу дату рождения (24.11.2000).")
    await Employer.date_of_birthday.set()


@dp.message_handler(state=User.date_of_birthday)
async def date_of_birthday_enter(msg: types.Message, state: FSMContext):
    try:
        today = datetime.date.today()
        birth = datetime.datetime.strptime(msg.text, "%d.%m.%Y").date()
        age = today.year - birth.year - ((today.month, today.day) < (birth.month, birth.day))
        if age >= 18:
            await state.update_data(date_of_birthday=birth)
            await msg.answer("Введите ваш номер телефона.")
            await Employer.phone.set()
        else:
            await msg.answer("Вам должно быть больше 18 лет! Подрастешь, потом зарегистрируешься.")
            await state.finish()
    except ValueError:
        await msg.answer("Введите корректную дату!")
        await Employer.date_of_birthday.set()


@dp.message_handler(state=User.phone)
async def phone_enter(msg: types.Message, state: FSMContext):
    phone = msg.text.strip()
    if fullmatch(r"^((\+7|7|8)+([0-9]){10})$", phone):
        await state.update_data(phone=phone)

        data = await state.get_data()
        match data.get("role"):
            case "Employer":
                await msg.answer("Введите номер и серию паспорта. (9011 567894).")
                await Employer.passport.set()
            case "Applicant":
                await msg.answer("Введите ваше образование.")
                await Applicant.education.set()
    else:
        await msg.answer("Введите номер телефона следующего формата: +79881234567")
        await Employer.phone.set()


@dp.message_handler(state=User.username)
async def username_enter(msg: types.Message, state: FSMContext):
    await state.update_data(username=msg.text)

    await msg.answer("Введите желаемый пароль.")

    await Employer.password.set()


@dp.message_handler(state=User.password)
async def password_enter(msg: types.Message, state: FSMContext):
    await state.update_data(password=msg.text)

    data = await state.get_data()
    try:
        match data.get("role"):
            case "Employer":
                await em_ser.add_employer(**data)

            case "Applicant":
                await ap_ser.addApplicant(**data)

    except UniqueViolationError:
        await msg.answer("Пользователь с таким именем уже существует. Введите новое имя!")
        await User.username.set()
        return

    await msg.answer("Вы успешно зарегистрировались!")
    await state.finish()


@dp.message_handler(state=Employer.passport)
async def passport_enter(msg: types.Message, state: FSMContext):
    passport = msg.text.strip()

    if fullmatch(r"\d{4} \d{6}", passport):
        await state.update_data(passport=passport)
        await msg.answer("Введите название вашей организации.")
        await Employer.organization_name.set()
    else:
        await msg.answer("Введите паспорт формата (9011 567894).")
        await Employer.passport.set()


@dp.message_handler(state=Employer.organization_name)
async def organization_name_enter(msg: types.Message, state: FSMContext):
    await state.update_data(organization_name=msg.text)

    await msg.answer("Введите желаемый логин.")

    await Employer.username.set()


@dp.message_handler(state=Applicant.education)
async def education_enter(msg: types.Message, state: FSMContext):
    await state.update_data(education=msg.text)

    await msg.answer("У вас есть права? (Да, Нет)")

    await Applicant.drive_license.set()


@dp.message_handler(state=Applicant.drive_license)
async def drive_license_enter(msg: types.Message, state: FSMContext):
    match msg.text.lower():
        case "да":
            await state.update_data(drive_license=True)
        case "нет":
            await state.update_data(drive_license=False)
        case _:
            await msg.answer("Ответ может быть только да или нет!. Введите заново.")
            await Applicant.drive_license.set()
            return

    await msg.answer("У вас есть военный билет? (Да, Нет)")

    await Applicant.military_ticket.set()


@dp.message_handler(state=Applicant.military_ticket)
async def military_ticket_enter(msg: types.Message, state: FSMContext):
    match msg.text.lower():
        case "да":
            await state.update_data(military_ticket=True)
        case "нет":
            await state.update_data(military_ticket=False)
        case _:
            await msg.answer("Ответ может быть только да или нет!. Введите заново.")
            await Applicant.military_ticket.set()
            return

    await msg.answer("Вы владеете английским языком? (Да, Нет)")
    await Applicant.english.set()


@dp.message_handler(state=Applicant.english)
async def english_enter(msg: types.Message, state: FSMContext):
    match msg.text.lower():
        case "да":
            await state.update_data(english=True)
        case "нет":
            await state.update_data(english=False)
        case _:
            await msg.answer("Ответ может быть только да или нет!. Введите заново.")
            await Applicant.english.set()
            return

    await msg.answer("Введите желаемый логин.")

    await Applicant.username.set()
