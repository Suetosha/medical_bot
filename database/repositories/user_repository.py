from sqlalchemy.ext.asyncio import AsyncSession
from database.models.user_model import User


class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, user_id: int) -> User | None:
        user = await self.session.get(User, user_id)
        return user

    async def add(self, user_id: int) -> None:
        self.session.add(User(telegram_id=user_id))
        await self.session.commit()

