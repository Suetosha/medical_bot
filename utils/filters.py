from aiogram.filters import Filter
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession
from database.repositories.faq_repository import FaqRepository
from database.fixtures.faq import Questions


class FAQFilter(Filter):
    async def __call__(self, message: Message, session: AsyncSession) -> bool:
        faq_repo = FaqRepository(session)
        questions = await faq_repo.get_questions()
        return message.text in questions

