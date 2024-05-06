from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.filters import StateFilter

from sqlalchemy.ext.asyncio import AsyncSession

from database.repositories.user_repository import UserRepository
from database.repositories.call_request_repository import CallRequestRepository

from utils.fsm import FSMFillRequestForm

from keyboards.main_keyboard import build_menu_keyboard
from keyboards.cancel_keyboard import build_cancel_keyboard

from lexicon.lexicon import CALL_REQUEST_LEXICON
from lexicon.lexicon import MAIN_MENU_LEXICON

router = Router()


@router.message(F.text == MAIN_MENU_LEXICON['call_request'], StateFilter(default_state))
async def call_request_command(message: Message, state: FSMContext):
    await state.set_state(FSMFillRequestForm.fill_name)
    await message.answer(CALL_REQUEST_LEXICON['fill_name'], reply_markup=build_cancel_keyboard())


@router.message(StateFilter(FSMFillRequestForm.fill_name))
async def fill_problem_command(message: Message, state: FSMContext):
    await state.set_state(FSMFillRequestForm.fill_problem)
    await state.update_data(name=message.text)
    await message.answer(CALL_REQUEST_LEXICON['fill_problem'], reply_markup=build_cancel_keyboard())


@router.message(StateFilter(FSMFillRequestForm.fill_problem))
async def fill_phone_number_command(message: Message, state: FSMContext):
    await state.set_state(FSMFillRequestForm.fill_phone_number)
    await state.update_data(problem=message.text)
    await message.answer(CALL_REQUEST_LEXICON['fill_phone_number'], reply_markup=build_cancel_keyboard())


@router.message(StateFilter(FSMFillRequestForm.fill_phone_number))
async def get_data_command(message: Message, state: FSMContext, session: AsyncSession):
    await state.update_data(phone_number=str(message.text))

    data = await state.get_data()

    call_request_repo = CallRequestRepository(session)
    await call_request_repo.add(data['name'], data['problem'], data['phone_number'])

    await state.clear()

    user_id = message.from_user.id
    user_repo = UserRepository(session)
    admin_status = await user_repo.get_admin_status(user_id)

    await message.answer(CALL_REQUEST_LEXICON['request_accepted'],
                         reply_markup=build_menu_keyboard(admin_status))




