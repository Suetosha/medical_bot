from aiogram.fsm.state import State, StatesGroup


class FSMFillFAQForm(StatesGroup):
    # Для создания часто задаваемого вопроса
    fill_question = State()
    fill_answer = State()

    # Для удаления часто задаваемого вопроса
    choose_faq = State()


class FSMFillRequestForm(StatesGroup):
    # Для добавления заявок
    fill_name = State()
    fill_problem = State()
    fill_phone_number = State()

    # Для вывода заявок в админ панели
    show_requests = State()

    # Для удаления заявки в админ панели
    delete_request = State()


class FSMFillServiceForm(StatesGroup):
    # Для добавления услуги
    fill_service = State()
    fill_answer = State()

    # Для удаления услуги в админ панели
    choose_service = State()


class FSMFillAppointmentForm(StatesGroup):
    # Для изменения записи в админ панели
    edit_appointment = State()
    update_object = State()

    # Для добавления/изменения записи в админ панели
    fill_specialization = State()
    fill_doctor = State()
    fill_date = State()
    fill_time = State()
    fill_name = State()
    fill_phone_number = State()

    # Для удаления записи в админ панели
    choose_appointment = State()


class FSMFillSlotForm(StatesGroup):
    # Для добавления слотов к врачу
    fill_department = State()
    fill_doctor = State()
    fill_time = State()

    # Для удаления слотов к врачу
    get_department = State()
    get_doctor = State()
    delete_slot_process = State()
