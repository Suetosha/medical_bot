from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.filters import StateFilter

from sqlalchemy.ext.asyncio import AsyncSession

from database.repositories.call_request_repository import CallRequestRepository
from utils.admin_status import get_admin_status
from utils.filters import AdminFilter

from utils.fsm import FSMFillRequestForm

from keyboards.keyboard_builder import kb_builder

from lexicon.lexicon import CALL_REQUEST_LEXICON, MAIN_KB_LEXICON, ADMIN_KB_LEXICON

router = Router()


# Процесс добавления заявки на звонок
@router.message(F.text == MAIN_KB_LEXICON['call_request'], StateFilter(default_state))
async def call_request_command(message: Message, state: FSMContext):
    await state.set_state(FSMFillRequestForm.fill_name)
    await message.answer(CALL_REQUEST_LEXICON['fill_name'], reply_markup=kb_builder(data=None, cancel_btn=True))


@router.message(StateFilter(FSMFillRequestForm.fill_name))
async def fill_problem_process(message: Message, state: FSMContext):
    await state.set_state(FSMFillRequestForm.fill_problem)
    await state.update_data(name=message.text)
    await message.answer(CALL_REQUEST_LEXICON['fill_problem'], reply_markup=kb_builder(data=None, cancel_btn=True))


@router.message(StateFilter(FSMFillRequestForm.fill_problem))
async def fill_phone_number_process(message: Message, state: FSMContext):
    await state.set_state(FSMFillRequestForm.fill_phone_number)
    await state.update_data(problem=message.text)
    await message.answer(CALL_REQUEST_LEXICON['fill_phone_number'], reply_markup=kb_builder(data=None, cancel_btn=True))


@router.message(StateFilter(FSMFillRequestForm.fill_phone_number))
async def get_data_process(message: Message, state: FSMContext, session: AsyncSession):
    await state.update_data(phone_number=str(message.text))

    data = await state.get_data()

    call_request_repo = CallRequestRepository(session)
    await call_request_repo.add(data['name'], data['problem'], data['phone_number'])

    await state.clear()

    admin_status = await get_admin_status(session=session, user_id=message.from_user.id)

    await message.answer(CALL_REQUEST_LEXICON['request_accepted'],
                         reply_markup=kb_builder(data=MAIN_KB_LEXICON, admin_status=admin_status))


# Процесс просмотра заявки на звонок в админ панели
@router.message(F.text == ADMIN_KB_LEXICON['show_call_requests'], AdminFilter())
async def choose_call_request_command(message: Message, session: AsyncSession, state: FSMContext):
    call_request_repo = CallRequestRepository(session)
    data = await call_request_repo.get_all()
    await state.set_state(FSMFillRequestForm.show_requests)
    await message.answer(CALL_REQUEST_LEXICON['choose_call_request'],
                         reply_markup=kb_builder(data=data, cancel_btn=True))


@router.message(StateFilter(FSMFillRequestForm.show_requests))
async def get_call_request_process(message: Message, session: AsyncSession):
    call_request_repo = CallRequestRepository(session)
    request_id, _ = message.text.split(', ')
    request = await call_request_repo.get_by_id(request_id=request_id)
    data = await call_request_repo.get_all()
    await message.answer(request, reply_markup=kb_builder(data=data, cancel_btn=True))


# Процесс удаления заявки на звонок в админ панели
@router.message(F.text == ADMIN_KB_LEXICON['delete_call_request'], AdminFilter())
async def choose_call_request_process(message: Message, session: AsyncSession, state: FSMContext):
    call_request_repo = CallRequestRepository(session)
    data = await call_request_repo.get_all()
    await state.set_state(FSMFillRequestForm.delete_request)
    await message.answer(CALL_REQUEST_LEXICON['choose_call_request_for_delete'],
                         reply_markup=kb_builder(data=data, cancel_btn=True))


@router.message(StateFilter(FSMFillRequestForm.delete_request))
async def delete_call_request_process(message: Message, session: AsyncSession):
    call_request_repo = CallRequestRepository(session)
    request_id, _ = message.text.split(', ')
    await call_request_repo.delete(request_id=request_id)
    data = await call_request_repo.get_all()
    await message.answer(CALL_REQUEST_LEXICON['call_request_deleted'], reply_markup=kb_builder(data=data,
                                                                                               cancel_btn=True))
