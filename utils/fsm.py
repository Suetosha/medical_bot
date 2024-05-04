from aiogram.fsm.state import State, StatesGroup


class FSMFillForm(StatesGroup):
    fill_question = State()
    fill_answer = State()
