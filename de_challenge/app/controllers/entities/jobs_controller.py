from app.controllers.controller import Controller
from app.database.entities.jobs import Job as JobData

class JobController(Controller):

    @staticmethod
    async def batch_from_csv(file: bytes, headers: list[str]):
        jobs = await JobController.read_csv_reader(file=file, headers=headers)
        return await JobData.insert_many(jobs=jobs)