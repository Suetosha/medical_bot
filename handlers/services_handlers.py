from aiogram import Router, F
from aiogram.types import Message

from sqlalchemy.ext.asyncio import AsyncSession

from lexicon.lexicon import MAIN_MENU_LEXICON
from lexicon.lexicon import SERVICES_LEXICON

from utils.filters import ServicesFilter

from database.repositories.service_repository import ServiceRepository

from keyboards.keyboard_builder import kb_builder


router = Router()


@router.message(F.text == MAIN_MENU_LEXICON['services'])
async def process_service_command(message: Message, session: AsyncSession):
    service_repo = ServiceRepository(session)
    data = await service_repo.get_services()
    await message.answer(SERVICES_LEXICON['choose_service'], reply_markup=kb_builder(data))


@router.message(ServicesFilter())
async def process_get_service_answer_command(message: Message, session: AsyncSession):
    service_repo = ServiceRepository(session)
    answer = (await service_repo.get_answer_by_service(message.text)).answer
    await message.answer(text=answer)
