from sqlalchemy.ext.asyncio import AsyncSession
from database.models import Doctor
from database.repositories.departments_repository import DepartmentsRepository
from sqlalchemy import select


class DoctorsRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add(self, name, department):
        dep_repo = DepartmentsRepository(self.session)
        department_id = await dep_repo.get_id_by_department_name(department)
        self.session.add(Doctor(name=name, department_id=department_id))
        await self.session.commit()

    async def get_all(self):
        data = (await self.session.scalars(select(Doctor))).all()
        data = [i.name for i in data]
        return data

    async def get_by_department(self, department):
        dep_repo = DepartmentsRepository(self.session)
        department_id = await dep_repo.get_id_by_department_name(department)
        doctors = (await self.session.execute(select(Doctor.name).filter_by(department_id=department_id))).fetchall()
        doctors = [i[0] for i in doctors]
        return doctors

    async def get_id_by_doctor(self, name):
        doctor_id = (await self.session.execute(select(Doctor).filter_by(name=name))).scalar_one().id
        return doctor_id

    async def get_doctor_by_id(self, doctor_id):
        doctor = (await self.session.execute(select(Doctor).filter_by(id=doctor_id))).scalar_one().name
        return doctor

    async def is_doctor_exist(self, doctor):
        doctors = await self.get_all()
        return doctor in doctors
