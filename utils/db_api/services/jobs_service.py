from asyncpg import UniqueViolationError

from models import JobModel


async def add_job(post: str, salary: float, chart: str, hours_in_week: float,
                  drive_license: bool, military_ticket: bool, english: bool,
                  employer_id: int):
    try:
        job = await JobModel.create(post=post, salary=salary, chart=chart,
                                    hours_in_week=hours_in_week, drive_license=drive_license,
                                    military_ticket=military_ticket, english=english,
                                    employer_id=employer_id)
        return job

    except UniqueViolationError:
        raise UniqueViolationError


async def get_all_jobs():
    jobs = await JobModel.query.gino.all()
    return jobs


async def get_all_jobs_by_employer(employer_id: int):
    jobs = await JobModel.query.where(JobModel.employer_id == employer_id).gino.all()
    return jobs


async def update_post(id: int, post: str):
    job = await JobModel.get(id)
    await job.update(post=post).apply()
    return job


async def update_salary(id: int, salary: float):
    job = await JobModel.get(id)
    await job.update(salary=salary).apply()
    return job


async def update_chart(id: int, chart: str):
    job = await JobModel.get(id)
    await job.update(chart=chart).apply()
    return job


async def update_hours_in_week(id: int, hours_in_week: float):
    job = await JobModel.get(id)
    await job.update(hours_in_week=hours_in_week).apply()
    return job


async def update_drive_license(id: int, drive_license: bool):
    job = await JobModel.get(id)
    await job.update(drive_license=drive_license).apply()
    return job


async def update_military_ticket(id: int, military_ticket: bool):
    job = await JobModel.get(id)
    await job.update(military_ticket=military_ticket).apply()
    return job


async def update_english(id: int, english: bool):
    job = await JobModel.get(id)
    await job.update(english=english).apply()
    return job


async def delete_job(id: int):
    job = await JobModel.get(id)
    await job.delete()
