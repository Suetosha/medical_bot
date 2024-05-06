from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import Message

from sqlalchemy.ext.asyncio import AsyncSession

from database.repositories.doctors_repository import DoctorsRepository
from keyboards.cancel_keyboard import build_cancel_keyboard
from lexicon.lexicon import MAIN_MENU_LEXICON
from lexicon.lexicon import APPOINTMENT_LEXICON

from database.repositories.departments_repository import DepartmentsRepository


from keyboards.main_keyboard import build_menu_keyboard
from keyboards.keyboard_builder import kb_builder
from utils.fsm import FSMFillAppointmentForm


router = Router()


@router.message(F.text == MAIN_MENU_LEXICON['appointment'], StateFilter(default_state))
async def appointment_command(message: Message, state: FSMContext, session: AsyncSession):
    depo_repo = DepartmentsRepository(session)
    data = await depo_repo.get_all_departments()
    await state.set_state(FSMFillAppointmentForm.fill_specialization)
    await message.answer(APPOINTMENT_LEXICON['choose_department'], reply_markup=kb_builder(data))


@router.message(StateFilter(FSMFillAppointmentForm.fill_specialization))
async def get_department_process(message: Message, session: AsyncSession, state: FSMContext,):
    await state.update_data(department=message.text)
    doctor_repo = DoctorsRepository(session)
    department = message.text
    doctors = await doctor_repo.get_doctors_by_department(department)

    await state.set_state(FSMFillAppointmentForm.fill_doctor)
    await message.answer(APPOINTMENT_LEXICON['choose_doctor'], reply_markup=kb_builder(doctors))

