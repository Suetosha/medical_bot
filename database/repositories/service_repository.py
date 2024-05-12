from sqlalchemy.ext.asyncio import AsyncSession
from database.models import Services
from sqlalchemy import select, delete


class ServiceRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add(self, service, answer):
        self.session.add(Services(service=service, answer=answer))
        await self.session.commit()

    async def get_services(self):
        data = (await self.session.scalars(select(Services))).all()
        data = [i.service for i in data]
        return data

    async def get_answer_by_service(self, service):
        answer = (await self.session.execute(select(Services).filter_by(service=service))).scalar_one()
        return answer

    async def delete_service(self, service):
        await self.session.execute(delete(Services).where(Services.service == service))
        await self.session.commit()
