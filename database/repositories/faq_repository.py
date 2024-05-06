from sqlalchemy.ext.asyncio import AsyncSession
from database.models import Faq
from sqlalchemy import select


class FaqRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add(self, question, answer):
        self.session.add(Faq(question=question, answer=answer))
        await self.session.commit()

    async def get_questions(self):
        data = (await self.session.scalars(select(Faq))).all()
        data = [i.question for i in data]
        return data

    async def get_answer_by_question(self, question):
        answer = (await self.session.execute(select(Faq).filter_by(question=question))).scalar_one()
        return answer
