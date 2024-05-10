from sqlalchemy.ext.asyncio import AsyncSession
from database.models import CallRequest


class CallRequestRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add(self, name, problem, phone_number):
        self.session.add(CallRequest(name=name, problem=problem, phone_number=phone_number))
        await self.session.commit()