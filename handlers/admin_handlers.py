from aiogram import Router, F
from aiogram.types import Message

from sqlalchemy.ext.asyncio import AsyncSession

from utils.admin_status import change_admin_status
from utils.filters import AdminFilter

from keyboards.keyboard_builder import kb_builder

from lexicon.lexicon import ADMIN_LEXICON, MAIN_KB_LEXICON, ADMIN_KB_LEXICON


router = Router()


@router.message(F.text == ADMIN_LEXICON['admin'])
async def process_admin_command(message: Message, session: AsyncSession):
    new_admin_status = await change_admin_status(session, message.from_user.id)
    await message.answer(ADMIN_LEXICON['admin_true'] if new_admin_status
                         else ADMIN_LEXICON['admin_false'], parse_mode="HTML",
                         reply_markup=kb_builder(data=MAIN_KB_LEXICON,
                                                 admin_status=new_admin_status, ))


@router.message(F.text == 'Панель администратора', AdminFilter())
async def admin_panel_command(message: Message):
    await message.answer(ADMIN_LEXICON['on_admin_panel'], reply_markup=kb_builder(data=list(ADMIN_KB_LEXICON.values()),
                                                                                  cancel_btn=True))


