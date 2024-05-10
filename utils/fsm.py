from aiogram.fsm.state import State, StatesGroup


class FSMFillFAQForm(StatesGroup):
    fill_question = State()
    fill_answer = State()


class FSMFillRequestForm(StatesGroup):
    fill_name = State()
    fill_problem = State()
    fill_phone_number = State()


class FSMFillServiceForm(StatesGroup):
    fill_service = State()
    fill_answer = State()


class FSMFillAppointmentForm(StatesGroup):
    # Для изменения записи в админке
    edit_appointment = State()
    update_object = State()

    # Для добавления/изменения записи
    fill_specialization = State()
    fill_doctor = State()
    fill_date = State()
    fill_time = State()
    fill_name = State()


class FSMFillSlotForm(StatesGroup):
    fill_department = State()
    fill_doctor = State()
    fill_time = State()


class FSMDeleteSlotForm(StatesGroup):
    fill_department = State()
    fill_doctor = State()
    delete_slot_process = State()





