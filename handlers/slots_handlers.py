from aiogram import Router, F
from aiogram.fsm.state import default_state
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter

from sqlalchemy.ext.asyncio import AsyncSession

from database.repositories.doctors_repository import DoctorsRepository
from database.repositories.slots_repository import SlotsRepository
from database.repositories.departments_repository import DepartmentsRepository

from utils.admin_status import get_admin_status

from keyboards.keyboard_builder import kb_builder

from utils.fsm import FSMFillSlotForm
from utils.filters import AdminFilter

from lexicon.lexicon import MAIN_KB_LEXICON, ADMIN_KB_LEXICON, SLOTS_LEXICON

import re


router = Router()


# Добавление нового слота к врачу
@router.message(F.text == ADMIN_KB_LEXICON['add_new_slot'], AdminFilter())
async def add_new_slots(message: Message, state: FSMContext, session: AsyncSession):
    dep_repo = DepartmentsRepository(session)
    departments = await dep_repo.get_all_departments()

    await state.set_state(FSMFillSlotForm.fill_department)
    await message.answer(SLOTS_LEXICON['fill_department'], reply_markup=kb_builder(data=departments, cancel_btn=True))


@router.message(StateFilter(FSMFillSlotForm.fill_department))
async def fill_department_process(message: Message, state: FSMContext, session: AsyncSession):
    department = message.text

    doc_repo = DoctorsRepository(session)
    doctors = await doc_repo.get_doctors_by_department(department)

    await state.set_state(FSMFillSlotForm.fill_doctor)
    await message.answer(SLOTS_LEXICON['fill_doctor'], reply_markup=kb_builder(data=doctors, cancel_btn=True))


@router.message(StateFilter(FSMFillSlotForm.fill_doctor))
async def get_doctor(message: Message, state: FSMContext, session: AsyncSession):
    doctor = message.text

    doc_repo = DoctorsRepository(session)
    doctor_id = await doc_repo.get_id_by_doctor(doctor)
    await state.update_data(doctor_id=doctor_id, doctor=doctor)

    await state.set_state(FSMFillSlotForm.fill_time)
    await message.answer(SLOTS_LEXICON['fill_time'], reply_markup=kb_builder(data=None, cancel_btn=True))


@router.message(StateFilter(FSMFillSlotForm.fill_time))
async def get_time(message: Message, state: FSMContext, session: AsyncSession):
    if re.fullmatch(r'([01]?[0-9]|2[0-3]):[0-5][0-9]', message.text):
        await state.update_data(time=message.text)
        doctor_id, doctor, time = (await state.get_data()).values()

        slots_repo = SlotsRepository(session)

        is_added = await slots_repo.add(doctor_id=doctor_id, time=time)

        await state.clear()

        admin_status = await get_admin_status(session=session, user_id=message.from_user.id)

        await message.answer(SLOTS_LEXICON['slot_added'].format(time, doctor) if is_added
                             else SLOTS_LEXICON['slot_already_added'],
                             reply_markup=kb_builder(data=MAIN_KB_LEXICON, admin_status=admin_status))
    else:
        await message.answer(SLOTS_LEXICON['wrong_time'])


# Удаление слотов у врача
@router.message(F.text == ADMIN_KB_LEXICON['delete_doctors_slot'], StateFilter(default_state), AdminFilter())
async def delete_slot_process(message: Message, state: FSMContext, session: AsyncSession):
    dep_repo = DepartmentsRepository(session)
    departments = await dep_repo.get_all_departments()

    await state.set_state(FSMFillSlotForm.get_department)
    await message.answer(SLOTS_LEXICON['fill_department'], reply_markup=kb_builder(data=departments, cancel_btn=True))


@router.message(StateFilter(FSMFillSlotForm.get_department))
async def fill_department_process(message: Message, state: FSMContext, session: AsyncSession):
    department = message.text

    doc_repo = DoctorsRepository(session)
    doctors = await doc_repo.get_doctors_by_department(department)

    await state.set_state(FSMFillSlotForm.get_doctor)
    await message.answer(SLOTS_LEXICON['fill_doctor'], reply_markup=kb_builder(data=doctors))


@router.message(StateFilter(FSMFillSlotForm.get_doctor))
async def fill_doctor_process(message: Message, state: FSMContext, session: AsyncSession):
    doctor = message.text

    doc_repo = DoctorsRepository(session)
    doctor_id = await doc_repo.get_id_by_doctor(doctor)
    await state.update_data(doctor_id=doctor_id)

    slots_repo = SlotsRepository(session)
    slots = await slots_repo.get_doctor_slots(doctor_id)

    await state.set_state(FSMFillSlotForm.delete_slot_process)
    await message.answer(SLOTS_LEXICON['delete_slot_process'], reply_markup=kb_builder(data=slots,
                                                                                       cancel_btn=True))


@router.message(StateFilter(FSMFillSlotForm.delete_slot_process))
async def delete_slot_process(message: Message, state: FSMContext, session: AsyncSession):
    await state.update_data(time=message.text)
    doctor_id, time = (await state.get_data()).values()

    slots_repo = SlotsRepository(session)
    await slots_repo.delete_slot(doctor_id=doctor_id, time=time)
    slots = await slots_repo.get_doctor_slots(doctor_id)
    await state.clear()
    await message.answer(SLOTS_LEXICON['slot_deleted'].format(time), reply_markup=kb_builder(data=slots,
                                                                                             cancel_btn=True))
