from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from keyboards.inline import callback_datas


async def create_edit_profile_kb(applicant_id: int):
    edit_profile_kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Изм. ФИО",
                              callback_data=callback_datas.profile_cb.new("FCs", applicant_id, "Applicant")),
         InlineKeyboardButton(text="Изм. дату рождения",
                              callback_data=callback_datas.profile_cb.new("birth", applicant_id, "Applicant"))],
        [InlineKeyboardButton(text="Изм. номер телефона",
                              callback_data=callback_datas.profile_cb.new("phone", applicant_id, "Applicant"))],
        [InlineKeyboardButton(text="Изм. образование",
                              callback_data=callback_datas.profile_cb.new("education", applicant_id, "Applicant")),
         InlineKeyboardButton(text="Изм. наличие водит. прав",
                              callback_data=callback_datas.profile_cb.new("drive_license", applicant_id, "Applicant"))],
        [InlineKeyboardButton(text="Изм. наличие военного билет",
                              callback_data=callback_datas.profile_cb.new("military_ticket", applicant_id, "Applicant"))],
        [InlineKeyboardButton(text="Изм. знание английского языка",
                              callback_data=callback_datas.profile_cb.new("english", applicant_id, "Applicant"))]
    ]
    )

    return edit_profile_kb


async def create_edit_job_kb(job_id: int):
    view_job_kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Получить информацию о работодателе",
                              callback_data=callback_datas.view_job_cb.new(job_id))]
    ])

    return view_job_kb
