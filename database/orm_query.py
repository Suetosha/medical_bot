from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from database.models import User


async def orm_add_user(session: AsyncSession, data: dict):
    telegram_id = data['telegram_id']
    user: User | None = await session.get(User, telegram_id)
    if user is None:
        session.add(User(telegram_id=data['telegram_id']))
        await session.commit()
