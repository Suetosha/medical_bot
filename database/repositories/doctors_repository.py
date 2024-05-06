from sqlalchemy.ext.asyncio import AsyncSession
from database.models import Doctors
from database.repositories.departments_repository import DepartmentsRepository
from sqlalchemy import select


class DoctorsRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add(self, doctor, department):
        dep_repo = DepartmentsRepository(self.session)
        department_id = await dep_repo.get_id_by_department_name(department)
        self.session.add(Doctors(doctor=doctor, department_id=department_id))
        await self.session.commit()

    async def get_all(self):
        data = (await self.session.scalars(select(Doctors))).all()
        data = [i.doctor for i in data]
        return data

    async def get_doctors_by_department(self, department):
        dep_repo = DepartmentsRepository(self.session)
        department_id = await dep_repo.get_id_by_department_name(department)
        doctors = (await self.session.execute(select(Doctors.doctor).filter_by(department_id=department_id))).fetchall()
        doctors = [i[0] for i in doctors]
        return doctors