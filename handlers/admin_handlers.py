from aiogram import Router, F
from aiogram.fsm.state import default_state
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession

from database.repositories.faq_repository import FaqRepository
from keyboards.admin_keyboard import build_admin_keyboard
from aiogram.filters import StateFilter
from utils.fsm import FSMFillForm


router = Router()


@router.message(F.text == 'Панель администратора')
async def process_admin_command(message: Message):
    await message.answer('Вы попали на панель администратора', reply_markup=build_admin_keyboard())


@router.message(F.text == 'Добавить FAQ', StateFilter(default_state))
async def fill_question(message: Message,  state: FSMContext):
    await message.answer('Напишите вопрос')
    await state.set_state(FSMFillForm.fill_question)


@router.message(StateFilter(FSMFillForm.fill_question))
async def fill_question(message: Message,  state: FSMContext):

    await state.update_data(question=message.text)
    await message.answer('Напишите ответ')
    await state.set_state(FSMFillForm.fill_answer)


@router.message(StateFilter(FSMFillForm.fill_answer))
async def fill_question(message: Message,  state: FSMContext, session: AsyncSession):
    await state.update_data(answer=message.text)

    faq_repo = FaqRepository(session)
    data = await state.get_data()

    await faq_repo.add(data['question'], data['answer'])

    await state.clear()
    await message.answer('Вопрос и ответ добавлены в бд')

