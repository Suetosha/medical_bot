from datetime import time, datetime

from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram_calendar import SimpleCalendar, SimpleCalendarCallback, get_user_locale

from sqlalchemy.ext.asyncio import AsyncSession

from lexicon.lexicon import MAIN_KB_LEXICON, ADMIN_KB_LEXICON
from lexicon.lexicon import APPOINTMENT_LEXICON

from database.repositories.departments_repository import DepartmentsRepository
from database.repositories.appointments_repository import AppointmentsRepository
from database.repositories.doctors_repository import DoctorsRepository
from database.repositories.slots_repository import SlotsRepository

from keyboards.keyboard_builder import kb_builder

from utils.admin_status import get_admin_status
from utils.filters import AdminFilter
from utils.fsm import FSMFillAppointmentForm

router = Router()


# Процесс записи к врачу
@router.message(F.text == MAIN_KB_LEXICON['appointment'], StateFilter(default_state))
async def main_appointment_command(message: Message, state: FSMContext, session: AsyncSession):
    depo_repo = DepartmentsRepository(session)
    data = await depo_repo.get_all()
    await state.set_state(FSMFillAppointmentForm.fill_specialization)
    await message.answer(APPOINTMENT_LEXICON['choose_department'], reply_markup=kb_builder(data=data, cancel_btn=True))


@router.message(StateFilter(FSMFillAppointmentForm.fill_specialization))
async def get_department_process(message: Message, session: AsyncSession, state: FSMContext):
    await state.update_data(department=message.text)

    doctor_repo = DoctorsRepository(session)
    department = message.text
    doctors = await doctor_repo.get_by_department(department)

    await state.set_state(FSMFillAppointmentForm.fill_doctor)
    await message.answer(APPOINTMENT_LEXICON['choose_doctor'], reply_markup=kb_builder(data=doctors, cancel_btn=True))


@router.message(StateFilter(FSMFillAppointmentForm.fill_doctor))
async def get_doctor_process(message: Message, state: FSMContext):
    await state.update_data(doctor=message.text)
    await state.set_state(FSMFillAppointmentForm.fill_date)

    calendar = await SimpleCalendar(await get_user_locale(message.from_user)).start_calendar()
    ReplyKeyboardRemove()
    await message.answer(APPOINTMENT_LEXICON['choose_date'],
                         reply_markup=calendar)


@router.callback_query(SimpleCalendarCallback.filter(), StateFilter(FSMFillAppointmentForm.fill_date))
async def get_date_process(callback_query: CallbackQuery, callback_data, state: FSMContext, session: AsyncSession):

    calendar = SimpleCalendar(
        locale=await get_user_locale(callback_query.from_user), show_alerts=True
    )

    selected, date = await calendar.process_selection(callback_query, callback_data)
    selected_date = date.date()

    slots_repo = SlotsRepository(session)
    app_repo = AppointmentsRepository(session)

    doctor_name = (await state.get_data())['doctor']

    all_slots = await slots_repo.get_doctor_slots(doctor_name)
    closed_slots = await app_repo.get_by_date_and_doctor_name(selected_date, doctor_name)
    free_slots = [i.strftime('%H:%M') for i in all_slots if i not in closed_slots]


    if selected and free_slots:
        await state.update_data(date=date)
        await state.set_state(FSMFillAppointmentForm.fill_time)
        await callback_query.message.answer(APPOINTMENT_LEXICON['choose_time']
                                            .format(date.strftime("%d/%m/%Y")),
                                            reply_markup=kb_builder(data=free_slots, cancel_btn=True))
    else:
        await callback_query.message.answer(APPOINTMENT_LEXICON['no_free_slots'],
                                            reply_markup=kb_builder(data=free_slots, cancel_btn=True))


@router.message(StateFilter(FSMFillAppointmentForm.fill_time))
async def get_time_process(message: Message, state: FSMContext):

    await state.update_data(time=message.text)
    await state.set_state(FSMFillAppointmentForm.fill_name)
    await message.answer(APPOINTMENT_LEXICON['fill_name'], reply_markup=ReplyKeyboardRemove())


@router.message(StateFilter(FSMFillAppointmentForm.fill_name))
async def get_name_process(message: Message, state: FSMContext):

    await state.update_data(name=message.text)
    await state.set_state(FSMFillAppointmentForm.fill_phone_number)
    await message.answer(APPOINTMENT_LEXICON['fill_phone_number'])


@router.message(StateFilter(FSMFillAppointmentForm.fill_phone_number))
async def get_phone_number_process(message: Message, state: FSMContext, session: AsyncSession):
    await state.update_data(phone_number=message.text)
    data = await state.get_data()

    hour, minutes = data['time'].split(':')
    app_time = time(int(hour), int(minutes))
    data['time'] = app_time
    app_date = data['date']

    app_repo = AppointmentsRepository(session)
    doctor_repo = DoctorsRepository(session)

    data['doctor_id'] = await doctor_repo.get_id_by_doctor(data['doctor'])

    admin_status = await get_admin_status(session=session, user_id=message.from_user.id)

    # Если необходимо отредактировать запись
    if 'id' in data.keys():
        await app_repo.update(data=data)
        await state.clear()
        await message.answer(APPOINTMENT_LEXICON['success_update'], reply_markup=kb_builder(data=MAIN_KB_LEXICON,
                                                                                            admin_status=admin_status))

    else:
    # Если необходимо добавить новую запись
        await app_repo.add(patient=data['name'], phone_number=data['phone_number'], doctor_id=data['doctor_id'],
                           date=app_date, time=app_time)

        await state.clear()
        await message.answer(APPOINTMENT_LEXICON['success'].
                             format(data['name'], data['date'].strftime("%d/%m/%Y"), data['time'], data['doctor']),
                             reply_markup=kb_builder(data=MAIN_KB_LEXICON, admin_status=admin_status))


# Редактирование записей
@router.message(F.text == ADMIN_KB_LEXICON['edit_appointment'], AdminFilter())
async def edit_appointment_command(message: Message, state: FSMContext, session: AsyncSession):
    app_repo = AppointmentsRepository(session)
    appointments = await app_repo.get_all()

    if appointments:
        await state.set_state(FSMFillAppointmentForm.edit_appointment)
        await message.answer(APPOINTMENT_LEXICON['choose_appointment'], reply_markup=kb_builder(data=appointments,
                                                                                                cancel_btn=True))
    else:
        await message.answer(APPOINTMENT_LEXICON['no_appointments'])


@router.message(StateFilter(FSMFillAppointmentForm.edit_appointment), AdminFilter())
async def get_appointment_info_process(message: Message, state: FSMContext, session: AsyncSession):
    id, patient = message.text.split(', ')

    app_repo = AppointmentsRepository(session)
    depo_repo = DepartmentsRepository(session)

    data = await depo_repo.get_all()
    app = await app_repo.get_by_id(id)


    await state.update_data(id=id)

    await state.set_state(FSMFillAppointmentForm.fill_specialization)
    await message.answer(APPOINTMENT_LEXICON['appointment_info'].format(app['department'], app['doctor'],
                                                                        app['date'], app['time'], app['patient']))

    await message.answer(APPOINTMENT_LEXICON['choose_department'], reply_markup=kb_builder(data=data, cancel_btn=True))


# Процесс удаления записи к врачу в админ панели
@router.message(F.text == ADMIN_KB_LEXICON['delete_appointment'], AdminFilter())
async def choose_appointment_process(message: Message, session: AsyncSession, state: FSMContext):
    app_repo = AppointmentsRepository(session)
    data = await app_repo.get_all()

    await state.set_state(FSMFillAppointmentForm.choose_appointment)
    await message.answer(APPOINTMENT_LEXICON['choose_appointment_for_delete'],
                         reply_markup=kb_builder(data=data, cancel_btn=True))


@router.message(StateFilter(FSMFillAppointmentForm.choose_appointment))
async def delete_appointment_process(message: Message, session: AsyncSession):
    app_repo = AppointmentsRepository(session)
    id, _ = message.text.split(', ')

    await app_repo.delete(app_id=int(id))

    data = await app_repo.get_all()
    await message.answer(APPOINTMENT_LEXICON['appointment_deleted'], reply_markup=kb_builder(data=data,
                                                                                             cancel_btn=True))
