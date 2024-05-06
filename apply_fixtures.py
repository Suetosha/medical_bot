import os
from dotenv import load_dotenv
from asyncio import run
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from database.repositories.faq_repository import FaqRepository
from database.repositories.service_repository import ServiceRepository

from database.fixtures.faq import Questions
from database.fixtures.services import Services


load_dotenv(dotenv_path='.env')

engine = create_async_engine(os.getenv('DB_LITE'), echo=True)
session_maker = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)


async def add_faq():
    async with session_maker() as session:
        faq_repo = FaqRepository(session)
        for question, answer in Questions.items():
            await faq_repo.add(question, answer)


async def add_services():
    async with session_maker() as session:
        services_repo = ServiceRepository(session)
        for service, answer in Services.items():
            await services_repo.add(service, answer)


async def main():
    await add_faq()
    await add_services()


if __name__ == '__main__':
    run(main())
