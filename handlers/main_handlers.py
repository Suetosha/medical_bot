from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, callback_query
from sqlalchemy.ext.asyncio import AsyncSession

from lexicon.lexicon import LEXICON

from database.orm_query import orm_add_user
from keyboards.main_keyboard import build_menu_keyboard

router = Router()


@router.message(CommandStart())
async def process_start_command(message: Message, session: AsyncSession):
    await orm_add_user(session, {'telegram_id': message.from_user.id})
    await message.answer(LEXICON['start'], reply_markup=build_menu_keyboard())


@router.message(F.text == 'Расписание работы клиники')
async def process_schedule_command(message: Message):
    await message.answer(LEXICON['clinic_schedule'])
