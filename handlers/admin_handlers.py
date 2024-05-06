from aiogram import Router, F
from aiogram.fsm.state import default_state
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter

from sqlalchemy.ext.asyncio import AsyncSession

from database.repositories.faq_repository import FaqRepository
from database.repositories.user_repository import UserRepository
from database.repositories.service_repository import ServiceRepository

from keyboards.admin_keyboard import build_admin_keyboard
from keyboards.main_keyboard import build_menu_keyboard

from utils.fsm import FSMFillFAQForm, FSMFillServiceForm
from utils.filters import AdminFilter

from lexicon.lexicon import ADMIN_LEXICON
from lexicon.lexicon import MAIN_MENU_LEXICON


router = Router()


@router.message(F.text == ADMIN_LEXICON['admin'])
async def process_admin_command(message: Message, session: AsyncSession):

    user_id = message.from_user.id
    user_repo = UserRepository(session)

    await user_repo.update_admin_status(user_id=user_id)
    admin_status = await user_repo.get_admin_status(user_id)

    await message.answer(ADMIN_LEXICON['admin_true'] if admin_status
                         else ADMIN_LEXICON['admin_false'], reply_markup=build_menu_keyboard(admin_status))


@router.message(F.text == MAIN_MENU_LEXICON['admin_panel'], AdminFilter())
async def admin_panel_command(message: Message, session: AsyncSession):
    await message.answer(ADMIN_LEXICON['on_admin_panel'], reply_markup=build_admin_keyboard())


# Часто задаваемые вопросы
@router.message(F.text == ADMIN_LEXICON['add_faq'], StateFilter(default_state), AdminFilter())
async def fill_question_command(message: Message,  state: FSMContext):
    await message.answer(ADMIN_LEXICON['fill_question'])
    await state.set_state(FSMFillFAQForm.fill_question)


@router.message(StateFilter(FSMFillFAQForm.fill_question))
async def fill_answer_command(message: Message,  state: FSMContext):

    await state.update_data(question=message.text)
    await message.answer(ADMIN_LEXICON['fill_answer'])
    await state.set_state(FSMFillFAQForm.fill_answer)


@router.message(StateFilter(FSMFillFAQForm.fill_answer))
async def add_faq_to_db(message: Message,  state: FSMContext, session: AsyncSession):
    await state.update_data(answer=message.text)

    faq_repo = FaqRepository(session)
    data = await state.get_data()

    await faq_repo.add(data['question'], data['answer'])

    await state.clear()
    await message.answer(ADMIN_LEXICON['added_to_db'])


# Добавить услугу
@router.message(F.text == ADMIN_LEXICON['add_service'], StateFilter(default_state), AdminFilter())
async def fill_service_command(message: Message,  state: FSMContext):
    await message.answer(ADMIN_LEXICON['fill_service'])
    await state.set_state(FSMFillServiceForm.fill_service)


@router.message(StateFilter(FSMFillServiceForm.fill_service))
async def fill_service_answer_command(message: Message,  state: FSMContext):
    await state.update_data(service=message.text)
    await message.answer(ADMIN_LEXICON['fill_service_answer'])
    await state.set_state(FSMFillServiceForm.fill_answer)


@router.message(StateFilter(FSMFillServiceForm.fill_answer))
async def add_service_to_db(message: Message,  state: FSMContext, session: AsyncSession):
    await state.update_data(answer=message.text)

    service_repo = ServiceRepository(session)
    data = await state.get_data()

    await service_repo.add(data['service'], data['answer'])

    await state.clear()
    await message.answer(ADMIN_LEXICON['added_to_db'])
