from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from database.models import CallRequest


class CallRequestRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add(self, name, problem, phone_number):
        self.session.add(CallRequest(name=name, problem=problem, phone_number=phone_number))
        await self.session.commit()

    async def get_call_requests(self):
        data = (await self.session.scalars(select(CallRequest))).all()
        data = [f'{i.id}, {i.name}' for i in data]
        return data

    async def get_call_request_by_id(self, id):
        request = (await self.session.execute(select(CallRequest).filter_by(id=id))).scalar_one()
        request = f'Имя: {request.name}\nПроблема: {request.problem}\nНомер телефона: {request.phone_number}'
        return request

    async def delete_call_request(self, id):
        await self.session.execute(delete(CallRequest).where(CallRequest.id == id))
        await self.session.commit()

