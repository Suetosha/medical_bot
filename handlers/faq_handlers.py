from aiogram import Router, F
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession
from lexicon.lexicon import LEXICON
from utils.filters import FAQFilter
from database.repositories.faq_repository import FaqRepository
from keyboards.faq_keyboard import faq_kb


router = Router()


@router.message(F.text == 'Часто задаваемые вопросы')
async def process_faq_command(message: Message, session: AsyncSession):
    faq_repo = FaqRepository(session)
    data = await faq_repo.get_questions()
    await message.answer('Выберите интересующий вас вопрос', reply_markup=faq_kb(data))


@router.message(FAQFilter())
async def process_get_answer_command(message: Message, session: AsyncSession):
    faq_repo = FaqRepository(session)
    answer = (await faq_repo.get_answer_by_question(message.text)).answer
    await message.answer(text=answer)


