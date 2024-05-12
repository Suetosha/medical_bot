from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state

from aiogram.types import Message

from sqlalchemy.ext.asyncio import AsyncSession

from lexicon.lexicon import SERVICES_LEXICON, MAIN_KB_LEXICON, ADMIN_KB_LEXICON

from database.repositories.service_repository import ServiceRepository

from keyboards.keyboard_builder import kb_builder

from utils.fsm import FSMFillServiceForm
from utils.admin_status import get_admin_status
from utils.filters import ServicesFilter, AdminFilter


router = Router()


# Процесс получения услуг
@router.message(F.text == MAIN_KB_LEXICON['services'])
async def process_service_command(message: Message, session: AsyncSession):
    service_repo = ServiceRepository(session)
    data = await service_repo.get_services()
    await message.answer(SERVICES_LEXICON['choose_service'], reply_markup=kb_builder(data=data, cancel_btn=True))


@router.message(ServicesFilter(), StateFilter(default_state))
async def process_get_service_answer_command(message: Message, session: AsyncSession):
    service_repo = ServiceRepository(session)
    answer = (await service_repo.get_answer_by_service(message.text)).answer
    await message.answer(text=answer, parse_mode="HTML")


# Добавить новую услугу
@router.message(F.text == ADMIN_KB_LEXICON['add_service'], StateFilter(default_state), AdminFilter())
async def fill_service_command(message: Message, state: FSMContext):
    await message.answer(SERVICES_LEXICON['fill_service'], reply_markup=kb_builder(data=None, cancel_btn=True))
    await state.set_state(FSMFillServiceForm.fill_service)


@router.message(StateFilter(FSMFillServiceForm.fill_service))
async def fill_service_answer_command(message: Message, state: FSMContext):
    await state.update_data(service=message.text)
    await message.answer(SERVICES_LEXICON['fill_service_answer'])
    await state.set_state(FSMFillServiceForm.fill_answer)


@router.message(StateFilter(FSMFillServiceForm.fill_answer))
async def add_service_to_db(message: Message, state: FSMContext, session: AsyncSession):
    await state.update_data(answer=message.text)

    service_repo = ServiceRepository(session)
    data = await state.get_data()

    await service_repo.add(data['service'], data['answer'])

    admin_status = await get_admin_status(session=session, user_id=message.from_user.id)

    await state.clear()
    await message.answer(SERVICES_LEXICON['added_to_db'], reply_markup=kb_builder(data=MAIN_KB_LEXICON,
                                                                                  admin_status=admin_status))


# Процесс удаления услуг через админ панель
@router.message(F.text == ADMIN_KB_LEXICON['delete_service'], AdminFilter())
async def process_choose_service_command(message: Message, session: AsyncSession, state: FSMContext):
    service_repo = ServiceRepository(session)
    data = await service_repo.get_services()
    await state.set_state(FSMFillServiceForm.choose_service)
    await message.answer(SERVICES_LEXICON['choose_service_for_delete'], reply_markup=kb_builder(data=data, cancel_btn=True))


@router.message(StateFilter(FSMFillServiceForm.choose_service))
async def process_delete_service_command(message: Message, session: AsyncSession):
    service_repo = ServiceRepository(session)
    await service_repo.delete_service(service=message.text)
    data = await service_repo.get_services()
    await message.answer(SERVICES_LEXICON['service_deleted'], reply_markup=kb_builder(data=data, cancel_btn=True))
