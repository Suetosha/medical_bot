import os
from dotenv import load_dotenv

from asyncio import run

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from database.repositories.faq_repository import FaqRepository
from database.repositories.service_repository import ServiceRepository
from database.repositories.departments_repository import DepartmentsRepository
from database.repositories.doctors_repository import DoctorsRepository

from database.fixtures.departments import Departments
from database.fixtures.doctors import Doctors
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


async def add_departments():
    async with session_maker() as session:
        depo_repo = DepartmentsRepository(session)
        [await depo_repo.add(department) for department in Departments]


async def add_doctors():
    async with session_maker() as session:
        doctors_repo = DoctorsRepository(session)
        for department, doctors in Doctors.items():
            for doctor_name in doctors:
                await doctors_repo.add(name=doctor_name, department=department)


async def main():
    await add_faq()
    await add_services()
    await add_departments()
    await add_doctors()


if __name__ == '__main__':
    run(main())
