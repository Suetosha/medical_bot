from sqlalchemy.ext.asyncio import AsyncSession
from database.models import Service
from sqlalchemy import select, delete


class ServiceRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add(self, service_name, answer):
        self.session.add(Service(name=service_name, answer=answer))
        await self.session.commit()

    async def get_all(self):
        data = (await self.session.scalars(select(Service))).all()
        data = [i.name for i in data]
        return data

    async def get_answer_by_service(self, service_name):
        answer = (await self.session.execute(select(Service).filter_by(name=service_name))).scalar_one()
        return answer

    async def delete(self, service_name):
        await self.session.execute(delete(Service).where(Service.name == service_name))
        await self.session.commit()
