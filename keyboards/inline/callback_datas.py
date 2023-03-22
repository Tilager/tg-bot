from aiogram.utils.callback_data import CallbackData

profile_cb = CallbackData("profile", "attribute", "id", "role")

job_cb = CallbackData("edit_job", "attribute", "job_id")

view_job_cb = CallbackData("view_job", "job_id")