from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboards.default import start_keyboards
from keyboards.inline.callback_datas import profile_cb
from loader import dp
from models import UserModel
from utils.db_api.services import user_service as us_ser


@dp.message_handler(text="Выйти")
async def logout(msg: types.Message):
    await us_ser.remove_user_id(msg.from_user.id)
    await msg.answer("Вы успешно вышли с аккаунта!", reply_markup=start_keyboards.not_auth_kb)


@dp.callback_query_handler(profile_cb.filter())
async def edit_profile(callback: types.CallbackQuery, callback_data: dict, state: FSMContext):
    await state.update_data(chat_id=callback.message.chat.id, message_id=callback.message.message_id,
                            profile_id=callback_data.get("id"))
    match callback_data.get("attribute"):
        case "FCs":
            await callback.answer()
            await callback.message.answer("Введите новое ФИО.")
            await state.set_state("profile:employer:FCs") if callback_data.get("role") == "Employer" \
                else await state.set_state("profile:applicant:FCs")

        case "birth":
            await callback.answer()
            await callback.message.answer("Введите новую дату рождения.")
            await state.set_state("profile:employer:birth") if callback_data.get("role") == "Employer" \
                else await state.set_state("profile:applicant:birth")

        case "phone":
            await callback.answer()
            await callback.message.answer("Введите новый номер телефона.")
            await state.set_state("profile:employer:phone") if callback_data.get("role") == "Employer" \
                else await state.set_state("profile:applicant:phone")

        case "passport":
            await callback.answer()
            await callback.message.answer("Введите новые паспортные данные.")
            await state.set_state("profile:employer:passport") if callback_data.get("role") == "Employer" \
                else await state.set_state("profile:applicant:passport")

        case "organization":
            await callback.answer()
            await callback.message.answer("Введите новое название организации.")
            await state.set_state("profile:employer:organization") if callback_data.get("role") == "Employer" \
                else await state.set_state("profile:applicant:organization")

        case "education":
            await callback.answer()
            await callback.message.answer("Введите ваше образование.")
            await state.set_state("profile:employer:education") if callback_data.get("role") == "Employer" \
                else await state.set_state("profile:applicant:education")

        case "drive_license":
            await callback.answer()
            await callback.message.answer("У вас есть водительские права? (Да, Нет)")
            await state.set_state("profile:employer:drive_license") if callback_data.get("role") == "Employer" \
                else await state.set_state("profile:applicant:drive_license")

        case "military_ticket":
            await callback.answer()
            await callback.message.answer("У вас есть военный билет? (Да, Нет)")
            await state.set_state("profile:employer:military_ticket") if callback_data.get("role") == "Employer" \
                else await state.set_state("profile:applicant:military_ticket")

        case "english":
            await callback.answer()
            await callback.message.answer("Вы знаете английский язык? (Да, Нет)")
            await state.set_state("profile:employer:english") if callback_data.get("role") == "Employer" \
                else await state.set_state("profile:applicant:english")
