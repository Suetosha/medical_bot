from datetime import datetime

from aiogram import Router, F
from aiogram.fsm.state import default_state
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter

from sqlalchemy.ext.asyncio import AsyncSession

from database.repositories.faq_repository import FaqRepository
from database.repositories.user_repository import UserRepository
from database.repositories.service_repository import ServiceRepository
from database.repositories.doctors_repository import DoctorsRepository
from database.repositories.slots_repository import SlotsRepository
from database.repositories.departments_repository import DepartmentsRepository
from database.repositories.appointments_repository import AppointmentsRepository
from utils.admin_status import change_admin_status

from keyboards.admin_keyboard import build_admin_keyboard
from keyboards.main_keyboard import build_menu_keyboard
from keyboards.cancel_keyboard import build_cancel_keyboard
from keyboards.keyboard_builder import kb_builder

from utils.fsm import FSMFillFAQForm, FSMFillServiceForm, FSMFillSlotForm, FSMDeleteSlotForm, \
    FSMFillAppointmentForm
from utils.filters import AdminFilter

from lexicon.lexicon import ADMIN_LEXICON, MAIN_MENU_LEXICON, APPOINTMENT_LEXICON

import re

router = Router()


@router.message(F.text == ADMIN_LEXICON['admin'])
async def process_admin_command(message: Message, session: AsyncSession):
    new_admin_status = await change_admin_status(session, message.from_user.id)
    await message.answer(ADMIN_LEXICON['admin_true'] if new_admin_status
                         else ADMIN_LEXICON['admin_false'], reply_markup=build_menu_keyboard(new_admin_status))


@router.message(F.text == MAIN_MENU_LEXICON['admin_panel'], AdminFilter())
async def admin_panel_command(message: Message):
    await message.answer(ADMIN_LEXICON['on_admin_panel'], reply_markup=build_admin_keyboard())


# Часто задаваемые вопросы
@router.message(F.text == ADMIN_LEXICON['add_faq'], StateFilter(default_state), AdminFilter())
async def fill_question_command(message: Message,  state: FSMContext):
    await message.answer(ADMIN_LEXICON['fill_question'])
    await state.set_state(FSMFillFAQForm.fill_question)


@router.message(StateFilter(FSMFillFAQForm.fill_question))
async def fill_answer_command(message: Message,  state: FSMContext):

    await state.update_data(question=message.text)
    await message.answer(ADMIN_LEXICON['fill_answer'])
    await state.set_state(FSMFillFAQForm.fill_answer)


@router.message(StateFilter(FSMFillFAQForm.fill_answer))
async def add_faq_to_db(message: Message,  state: FSMContext, session: AsyncSession):
    await state.update_data(answer=message.text)

    faq_repo = FaqRepository(session)
    data = await state.get_data()

    await faq_repo.add(data['question'], data['answer'])

    await state.clear()
    await message.answer(ADMIN_LEXICON['added_to_db'])


# Добавить услугу
@router.message(F.text == ADMIN_LEXICON['add_service'], StateFilter(default_state), AdminFilter())
async def fill_service_command(message: Message,  state: FSMContext):
    await message.answer(ADMIN_LEXICON['fill_service'])
    await state.set_state(FSMFillServiceForm.fill_service)


@router.message(StateFilter(FSMFillServiceForm.fill_service))
async def fill_service_answer_command(message: Message,  state: FSMContext):
    await state.update_data(service=message.text)
    await message.answer(ADMIN_LEXICON['fill_service_answer'])
    await state.set_state(FSMFillServiceForm.fill_answer)


@router.message(StateFilter(FSMFillServiceForm.fill_answer))
async def add_service_to_db(message: Message,  state: FSMContext, session: AsyncSession):
    await state.update_data(answer=message.text)

    service_repo = ServiceRepository(session)
    data = await state.get_data()

    await service_repo.add(data['service'], data['answer'])

    await state.clear()
    await message.answer(ADMIN_LEXICON['added_to_db'])


# Добавление нового слота к врачу
@router.message(F.text == ADMIN_LEXICON['add_new_slot'], StateFilter(default_state), AdminFilter())
async def add_new_slots(message: Message, state: FSMContext, session: AsyncSession):
    dep_repo = DepartmentsRepository(session)
    departments = await dep_repo.get_all_departments()

    await message.answer(ADMIN_LEXICON['fill_department'], reply_markup=kb_builder(departments))
    await state.set_state(FSMFillSlotForm.fill_department)


@router.message(StateFilter(FSMFillSlotForm.fill_department))
async def fill_department_process(message: Message, state: FSMContext, session: AsyncSession):
    department = message.text

    doc_repo = DoctorsRepository(session)
    doctors = await doc_repo.get_doctors_by_department(department)

    await state.set_state(FSMFillSlotForm.fill_doctor)
    await message.answer(ADMIN_LEXICON['fill_doctor'], reply_markup=kb_builder(doctors))


@router.message(StateFilter(FSMFillSlotForm.fill_doctor))
async def get_doctor(message: Message, state: FSMContext, session: AsyncSession):
    doctor = message.text

    doc_repo = DoctorsRepository(session)
    doctor_id = await doc_repo.get_id_by_doctor(doctor)
    await state.update_data(doctor_id=doctor_id, doctor=doctor)

    await state.set_state(FSMFillSlotForm.fill_time)
    await message.answer(ADMIN_LEXICON['fill_time'], reply_markup=build_cancel_keyboard())


@router.message(StateFilter(FSMFillSlotForm.fill_time))
async def get_time(message: Message, state: FSMContext, session: AsyncSession):

    if re.fullmatch(r'([01]?[0-9]|2[0-3]):[0-5][0-9]', message.text):
        await state.update_data(time=message.text)
        doctor_id, doctor, time = (await state.get_data()).values()

        slots_repo = SlotsRepository(session)
        is_copy_exists = await slots_repo.add_slots(doctor_id=doctor_id, time=time)

        await state.clear()
        user_repo = UserRepository(session)
        admin_status = await user_repo.get_admin_status(message.from_user.id)
        await message.answer(ADMIN_LEXICON['slot_added'].format(time, doctor) if not is_copy_exists
                             else ADMIN_LEXICON['slot_already_added'],
                             reply_markup=build_menu_keyboard(admin_status))

    else:
        await message.answer(ADMIN_LEXICON['wrong_time'])


# Удаление слотов у врача
@router.message(F.text == ADMIN_LEXICON['delete_doctors_slot'], StateFilter(default_state), AdminFilter())
async def delete_slot_process(message: Message, state: FSMContext, session: AsyncSession):
    dep_repo = DepartmentsRepository(session)
    departments = await dep_repo.get_all_departments()

    await state.set_state(FSMDeleteSlotForm.fill_department)
    await message.answer(ADMIN_LEXICON['fill_department'], reply_markup=kb_builder(departments))


@router.message(StateFilter(FSMDeleteSlotForm.fill_department))
async def fill_department_process(message: Message, state: FSMContext, session: AsyncSession):
    department = message.text

    doc_repo = DoctorsRepository(session)
    doctors = await doc_repo.get_doctors_by_department(department)

    await state.set_state(FSMDeleteSlotForm.fill_doctor)
    await message.answer(ADMIN_LEXICON['fill_doctor'], reply_markup=kb_builder(doctors))


@router.message(StateFilter(FSMDeleteSlotForm.fill_doctor))
async def fill_doctor_process(message: Message, state: FSMContext, session: AsyncSession):
    doctor = message.text

    doc_repo = DoctorsRepository(session)
    doctor_id = await doc_repo.get_id_by_doctor(doctor)
    await state.update_data(doctor_id=doctor_id)

    slots_repo = SlotsRepository(session)
    slots = await slots_repo.get_doctor_slots(doctor_id)

    await state.set_state(FSMDeleteSlotForm.delete_slot_process)
    await message.answer(ADMIN_LEXICON['delete_slot_process'], reply_markup=kb_builder(slots))


@router.message(StateFilter(FSMDeleteSlotForm.delete_slot_process))
async def delete_slot_process(message: Message, state: FSMContext, session: AsyncSession):
    await state.update_data(time=message.text)
    doctor_id, time = (await state.get_data()).values()

    slots_repo = SlotsRepository(session)
    await slots_repo.delete_slot(doctor_id=doctor_id, time=time)
    slots = await slots_repo.get_doctor_slots(doctor_id)
    await state.clear()
    await message.answer(ADMIN_LEXICON['slot_removed'].format(time), reply_markup=kb_builder(slots))


# Редактирование записей

@router.message(F.text == ADMIN_LEXICON['edit_appointment'], AdminFilter())
async def edit_appointment_process(message: Message, state: FSMContext, session: AsyncSession):
    app_repo = AppointmentsRepository(session)
    appointments = await app_repo.get_appointments()

    if appointments:
        await state.set_state(FSMFillAppointmentForm.edit_appointment)
        await message.answer(ADMIN_LEXICON['choose_appointment'], reply_markup=kb_builder(appointments))

    else:
        await message.answer(ADMIN_LEXICON['no_appointments'])


@router.message(StateFilter(FSMFillAppointmentForm.edit_appointment), AdminFilter())
async def get_appointment_info(message: Message, state: FSMContext, session: AsyncSession):
    id, patient = message.text.split(', ')

    app_repo = AppointmentsRepository(session)
    depo_repo = DepartmentsRepository(session)
    doc_repo = DoctorsRepository(session)

    data = await depo_repo.get_all_departments()

    app = await app_repo.get_appointment_by_id(id)

    department = await depo_repo.get_department_by_id(app.department_id)
    doctor = await doc_repo.get_doctor_by_id(app.doctor_id)
    date = datetime.strftime(app.date_time, '%d/%m/%Y')
    time = datetime.strftime(app.date_time, '%H:%M')

    await state.update_data(id=id)
    await state.set_state(FSMFillAppointmentForm.fill_specialization)
    await message.answer(ADMIN_LEXICON['appointment_info'].format(department, doctor, date, time, patient))
    await message.answer(APPOINTMENT_LEXICON['choose_department'], reply_markup=kb_builder(data))















