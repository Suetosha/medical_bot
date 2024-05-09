from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from sqlalchemy.ext.asyncio import AsyncSession

from lexicon.lexicon import START_COMMAND, CLINIC_SCHEDULE, CONTACT_INFORMATION
from lexicon.lexicon import MAIN_MENU_LEXICON

from database.repositories.user_repository import UserRepository

from keyboards.main_keyboard import build_menu_keyboard

router = Router()


@router.message(CommandStart())
async def process_start_command(message: Message, session: AsyncSession, state: FSMContext):
    user_repo = UserRepository(session)
    user_id = message.from_user.id

    if await user_repo.get_by_id(user_id) is None:
        await user_repo.add(user_id)

    admin_status = await user_repo.get_admin_status(user_id)
    await state.clear()
    await message.answer(START_COMMAND['info'], reply_markup=build_menu_keyboard(admin_status))


@router.message(F.text == MAIN_MENU_LEXICON['cancel'])
async def process_cancel_command(message: Message, state: FSMContext, session: AsyncSession):

    user_id = message.from_user.id
    user_repo = UserRepository(session)
    admin_status = await user_repo.get_admin_status(user_id)

    await state.clear()
    await message.answer(MAIN_MENU_LEXICON['main_menu'], reply_markup=build_menu_keyboard(admin_status))


@router.message(F.text == MAIN_MENU_LEXICON['clinic_schedule'])
async def process_schedule_command(message: Message):
    await message.answer(CLINIC_SCHEDULE['info'])


@router.message(F.text == MAIN_MENU_LEXICON['contact_information'])
async def process_schedule_command(message: Message):
    await message.answer(CONTACT_INFORMATION['info'])





