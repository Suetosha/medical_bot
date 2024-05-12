from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import Message

from sqlalchemy.ext.asyncio import AsyncSession

from lexicon.lexicon import FAQ_LEXICON, MAIN_KB_LEXICON, ADMIN_KB_LEXICON

from utils.admin_status import get_admin_status
from utils.filters import FAQFilter, AdminFilter
from utils.fsm import FSMFillFAQForm

from database.repositories.faq_repository import FaqRepository

from keyboards.keyboard_builder import kb_builder


router = Router()


# Процесс получения часто задаваемых вопросов
@router.message(F.text == MAIN_KB_LEXICON['faq'])
async def process_faq_command(message: Message, session: AsyncSession):
    faq_repo = FaqRepository(session)
    data = await faq_repo.get_questions()
    await message.answer(FAQ_LEXICON['choose_faq'], reply_markup=kb_builder(data=data, cancel_btn=True))


@router.message(FAQFilter())
async def process_get_answer_command(message: Message, session: AsyncSession):
    faq_repo = FaqRepository(session)
    answer = (await faq_repo.get_answer_by_question(message.text)).answer
    await message.answer(text=answer, parse_mode="HTML")


# Добавление часто задаваемых вопросов
@router.message(F.text == ADMIN_KB_LEXICON['add_faq'], AdminFilter())
async def fill_question_command(message: Message, state: FSMContext):
    await message.answer(FAQ_LEXICON['fill_question'], reply_markup=kb_builder(data=None, cancel_btn=True))
    await state.set_state(FSMFillFAQForm.fill_question)


@router.message(StateFilter(FSMFillFAQForm.fill_question))
async def fill_answer_command(message: Message, state: FSMContext):
    await state.update_data(question=message.text)
    await message.answer(FAQ_LEXICON['fill_answer'])
    await state.set_state(FSMFillFAQForm.fill_answer)


@router.message(StateFilter(FSMFillFAQForm.fill_answer))
async def add_faq_to_db(message: Message, state: FSMContext, session: AsyncSession):
    await state.update_data(answer=message.text)

    faq_repo = FaqRepository(session)
    data = await state.get_data()

    await faq_repo.add(data['question'], data['answer'])

    admin_status = await get_admin_status(session=session, user_id=message.from_user.id)

    await state.clear()
    await message.answer(FAQ_LEXICON['added_to_db'], reply_markup=kb_builder(data=MAIN_KB_LEXICON,
                                                                               admin_status=admin_status))


# Процесс удаления часто задаваемых вопросов в админ панели
@router.message(F.text == ADMIN_KB_LEXICON['delete_faq'], AdminFilter())
async def process_choose_faq_command(message: Message, session: AsyncSession, state: FSMContext):
    faq_repo = FaqRepository(session)
    data = await faq_repo.get_questions()
    await state.set_state(FSMFillFAQForm.choose_faq)
    await message.answer(FAQ_LEXICON['choose_faq_for_delete'], reply_markup=kb_builder(data=data, cancel_btn=True))


@router.message(StateFilter(FSMFillFAQForm.choose_faq))
async def process_delete_faq_command(message: Message, session: AsyncSession):
    faq_repo = FaqRepository(session)
    await faq_repo.delete_faq(question=message.text)
    data = await faq_repo.get_questions()
    await message.answer(FAQ_LEXICON['faq_deleted'], reply_markup=kb_builder(data=data, cancel_btn=True))
