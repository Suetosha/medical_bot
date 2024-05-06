from aiogram import Router, F
from aiogram.types import Message

from sqlalchemy.ext.asyncio import AsyncSession

from lexicon.lexicon import MAIN_MENU_LEXICON
from lexicon.lexicon import FAQ_LEXICON

from utils.filters import FAQFilter

from database.repositories.faq_repository import FaqRepository

from keyboards.faq_or_sevices_keyboard import kb_builder


router = Router()


@router.message(F.text == MAIN_MENU_LEXICON['faq'])
async def process_faq_command(message: Message, session: AsyncSession):
    faq_repo = FaqRepository(session)
    data = await faq_repo.get_questions()
    await message.answer(FAQ_LEXICON['choose_faq'], reply_markup=kb_builder(data))


@router.message(FAQFilter())
async def process_get_answer_command(message: Message, session: AsyncSession):
    faq_repo = FaqRepository(session)
    answer = (await faq_repo.get_answer_by_question(message.text)).answer
    await message.answer(text=answer)


