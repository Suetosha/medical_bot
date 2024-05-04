import os
from dotenv import load_dotenv
from asyncio import run
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from database.repositories.faq_repository import FaqRepository
from database.fixtures.faq import Questions

load_dotenv(dotenv_path='.env')

engine = create_async_engine(os.getenv('DB_LITE'), echo=True)
session_maker = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)


async def add_faq():
    async with session_maker() as session:
        faq_repo = FaqRepository(session)
        for question, answer in Questions.items():
            await faq_repo.add(question, answer)


async def main():
    await add_faq()


if __name__ == '__main__':
    run(main())
