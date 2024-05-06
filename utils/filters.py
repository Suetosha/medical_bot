from aiogram.filters import Filter
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession
from database.repositories.faq_repository import FaqRepository
from database.repositories.service_repository import ServiceRepository
from database.repositories.user_repository import UserRepository


class FAQFilter(Filter):
    async def __call__(self, message: Message, session: AsyncSession) -> bool:
        faq_repo = FaqRepository(session)
        questions = await faq_repo.get_questions()
        return message.text in questions



class ServicesFilter(Filter):
    async def __call__(self, message: Message, session: AsyncSession) -> bool:
        service_repo = ServiceRepository(session)
        services = await service_repo.get_services()
        return message.text in services


class AdminFilter(Filter):
    async def __call__(self, message: Message, session: AsyncSession) -> bool:
        user_repo = UserRepository(session)
        user_id = message.from_user.id
        admin_status = await user_repo.get_admin_status(user_id)

        return admin_status is True
