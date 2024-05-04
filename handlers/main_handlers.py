from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from lexicon.lexicon import LEXICON

from database.repositories.user_repository import UserRepository
from keyboards.main_keyboard import build_menu_keyboard

router = Router()


@router.message(CommandStart())
async def process_start_command(message: Message, session: AsyncSession):
    user_repo = UserRepository(session)

    if await user_repo.get_by_id(message.from_user.id) is None:
        await user_repo.add(message.from_user.id)

    await message.answer(LEXICON['start'], reply_markup=build_menu_keyboard())


@router.message(F.text == 'Расписание работы клиники')
async def process_schedule_command(message: Message):
    await message.answer(LEXICON['clinic_schedule'])
