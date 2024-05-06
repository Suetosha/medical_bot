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

