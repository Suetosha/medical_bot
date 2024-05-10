from sqlalchemy.ext.asyncio import AsyncSession
from database.models import Departments
from sqlalchemy import select


class DepartmentsRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add(self, specialization):
        self.session.add(Departments(specialization=specialization))
        await self.session.commit()

    async def get_id_by_department_name(self, department):
        department_id = (await self.session.execute(select(Departments)
                                                    .filter_by(specialization=department))).scalar_one().id
        return department_id

    async def get_all_departments(self):
        data = (await self.session.scalars(select(Departments))).all()
        data = [i.specialization for i in data]
        return data

    async def get_department_by_id(self, id):
        department = (await self.session.execute(select(Departments).filter_by(id=id))).scalar_one().specialization
        return department
