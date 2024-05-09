from sqlalchemy.ext.asyncio import AsyncSession
from database.models import User
from sqlalchemy import update


class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, user_id: int) -> User | None:
        user = await self.session.get(User, user_id)
        return user

    async def add(self, user_id: int) -> None:
        self.session.add(User(telegram_id=user_id))
        await self.session.commit()

    async def get_admin_status(self, user_id: int) -> User:
        status = (await self.get_by_id(user_id)).is_admin
        return status

    async def update_admin_status(self, user_id: int) -> None:
        status = await self.get_admin_status(user_id)
        new_status = False if status else True
        await self.session.execute(update(User).where(User.telegram_id == user_id).values(is_admin=new_status))
        await self.session.commit()

