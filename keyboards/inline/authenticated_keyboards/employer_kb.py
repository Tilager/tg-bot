from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from keyboards.inline import callback_datas


async def create_edit_profile_kb(employer_id: int):
    edit_profile_kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Изм. ФИО",
                              callback_data=callback_datas.profile_cb.new("FCs", employer_id, "Employer")),
         InlineKeyboardButton(text="Изм. дату рождения",
                              callback_data=callback_datas.profile_cb.new("birth", employer_id, "Employer"))],
        [InlineKeyboardButton(text="Изм. номер телефона",
                              callback_data=callback_datas.profile_cb.new("phone", employer_id, "Employer"))],
        [InlineKeyboardButton(text="Изм. паспорт",
                              callback_data=callback_datas.profile_cb.new("passport", employer_id, "Employer")),
         InlineKeyboardButton(text="Изм. название организации",
                              callback_data=callback_datas.profile_cb.new("organization", employer_id, "Employer"))]
    ])

    return edit_profile_kb


async def create_edit_job_kb(job_id: int):
    edit_job_kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Изм. должность",
                              callback_data=callback_datas.job_cb.new("post", job_id)),
         InlineKeyboardButton(text="Изм. зарплату",
                              callback_data=callback_datas.job_cb.new("salary", job_id))],
        [InlineKeyboardButton(text="Изм. график",
                              callback_data=callback_datas.job_cb.new("chart", job_id)),
         InlineKeyboardButton(text="Изм. количество рабочих часов",
                              callback_data=callback_datas.job_cb.new("hours", job_id))],
        [InlineKeyboardButton(text="Изм. наличие вод. прав",
                              callback_data=callback_datas.job_cb.new("drive_license", job_id)),
         InlineKeyboardButton(text="Изм. наличие военного билета",
                              callback_data=callback_datas.job_cb.new("military_ticket", job_id))],
        [InlineKeyboardButton(text="Изм. знание английского",
                              callback_data=callback_datas.job_cb.new("english", job_id)),
         InlineKeyboardButton(text="Удалить",
                              callback_data=callback_datas.job_cb.new("delete", job_id))]
    ])
    return edit_job_kb
