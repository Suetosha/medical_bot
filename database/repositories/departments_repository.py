from sqlalchemy.ext.asyncio import AsyncSession
from database.models import Department
from sqlalchemy import select


class DepartmentsRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add(self, department_name):
        self.session.add(Department(name=department_name))
        await self.session.commit()

    async def get_id_by_department_name(self, department_name):
        department_id = (await self.session.execute(select(Department)
                                                    .filter_by(name=department_name))).scalar_one().id
        return department_id

    async def get_all(self):
        data = (await self.session.scalars(select(Department))).all()
        data = [i.name for i in data]
        return data

    async def get_by_id(self, department_id):
        department = (await self.session.execute(select(Department).filter_by(id=department_id))).scalar_one().name
        return department
