from aiogram import Router, F

from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from sqlalchemy.ext.asyncio import AsyncSession

from lexicon.lexicon import START_COMMAND, CLINIC_SCHEDULE, CONTACT_INFORMATION
from lexicon.lexicon import MAIN_MENU_LEXICON, MAIN_KB_LEXICON

from database.repositories.user_repository import UserRepository

from keyboards.keyboard_builder import kb_builder
from utils.admin_status import get_admin_status

router = Router()


@router.message(CommandStart())
async def process_start_command(message: Message, session: AsyncSession, state: FSMContext):
    user_repo = UserRepository(session)
    user_id = message.from_user.id

    if await user_repo.get_by_id(user_id) is None:
        await user_repo.add(user_id)

    admin_status = await user_repo.get_admin_status(user_id)
    await state.clear()
    await message.answer(START_COMMAND['info'], parse_mode="HTML", reply_markup=kb_builder(data=MAIN_KB_LEXICON,
                                                                                           admin_status=admin_status))


@router.message(F.text == 'Отменить')
async def process_cancel_command(message: Message, state: FSMContext, session: AsyncSession):
    admin_status = await get_admin_status(session=session, user_id=message.from_user.id)
    await state.clear()
    await message.answer(MAIN_MENU_LEXICON['main_menu'], reply_markup=kb_builder(data=MAIN_KB_LEXICON,
                                                                                 admin_status=admin_status))


@router.message(F.text == MAIN_KB_LEXICON['clinic_schedule'])
async def process_schedule_command(message: Message):
    await message.answer(CLINIC_SCHEDULE['info'], parse_mode="HTML")


@router.message(F.text == MAIN_KB_LEXICON['contact_information'])
async def process_schedule_command(message: Message):
    await message.answer(CONTACT_INFORMATION['info'], parse_mode="HTML")





