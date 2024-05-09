import datetime
from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram_calendar import SimpleCalendar, SimpleCalendarCallback, get_user_locale
from sqlalchemy.ext.asyncio import AsyncSession
from database.repositories.doctors_repository import DoctorsRepository
from database.repositories.slots_repository import SlotsRepository
from database.repositories.user_repository import UserRepository
from lexicon.lexicon import MAIN_MENU_LEXICON
from lexicon.lexicon import APPOINTMENT_LEXICON

from database.repositories.departments_repository import DepartmentsRepository
from database.repositories.appointments_repository import AppointmentsRepository

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
async def get_department_process(message: Message, session: AsyncSession, state: FSMContext):
    await state.update_data(department=message.text)

    doctor_repo = DoctorsRepository(session)
    department = message.text
    doctors = await doctor_repo.get_doctors_by_department(department)

    await state.set_state(FSMFillAppointmentForm.fill_doctor)
    await message.answer(APPOINTMENT_LEXICON['choose_doctor'], reply_markup=kb_builder(doctors))


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

    slots_repo = SlotsRepository(session)
    doc_repo = DoctorsRepository(session)

    doctor = (await state.get_data())['doctor']
    doctor_id = await doc_repo.get_id_by_doctor(doctor)
    day = date.day

    free_slots = await slots_repo.get_opened_slots(day, doctor_id)

    if selected and free_slots:
        await state.update_data(date=date)
        await state.set_state(FSMFillAppointmentForm.fill_time)
        await callback_query.message.answer(APPOINTMENT_LEXICON['choose_time']
                                            .format(date.strftime("%d/%m/%Y")), reply_markup=kb_builder(free_slots))
    else:
        await callback_query.message.answer(APPOINTMENT_LEXICON['no_free_slots'], reply_markup=kb_builder(free_slots))


@router.message(StateFilter(FSMFillAppointmentForm.fill_time))
async def get_time_process(message: Message, state: FSMContext, session: AsyncSession):

    await state.update_data(time=message.text)
    await state.set_state(FSMFillAppointmentForm.fill_name)
    await message.answer(APPOINTMENT_LEXICON['fill_name'], reply_markup=ReplyKeyboardRemove())


@router.message(StateFilter(FSMFillAppointmentForm.fill_name))
async def get_phone_number_process(message: Message, state: FSMContext, session: AsyncSession):
    await state.update_data(name=message.text)
    data = await state.get_data()

    hours, minutes = data['time'].split(':')
    time_change = datetime.timedelta(hours=int(hours), minutes=int(minutes))
    data['date'] = data['date'] + time_change

    app_repo = AppointmentsRepository(session)
    depo_repo = DepartmentsRepository(session)
    doctor_repo = DoctorsRepository(session)
    user_repo = UserRepository(session)

    data['department_id'] = await depo_repo.get_id_by_department_name(data['department'])
    data['doctor_id'] = await doctor_repo.get_id_by_doctor(data['doctor'])

    admin_status = await user_repo.get_admin_status(message.from_user.id)

    if 'id' in data.keys():
        await app_repo.update_appointment(data=data)
        await state.clear()
        await message.answer(APPOINTMENT_LEXICON['success_update'], reply_markup=build_menu_keyboard(admin_status))

    else:

        await app_repo.add(patient=data['name'], department_id=data['department_id'], doctor_id=data['doctor_id'],
                           datetime=data['date'])
        await state.clear()
        await message.answer(APPOINTMENT_LEXICON['success'].
                             format(data['name'], data['date'].strftime("%d/%m/%Y"), data['time'], data['doctor']),
                             reply_markup=build_menu_keyboard(admin_status))
