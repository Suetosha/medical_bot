
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


def kb_builder(data: None | dict | list, cancel_btn=False, admin_status=False):
    buttons = []

    if data is not None:
        if type(data) is dict:
            buttons.extend([KeyboardButton(text=text) for text in data.values()])
            rows, cols = 3, 2
            cols_per_row = 2
            buttons = [[buttons[i * cols_per_row + j] for j in range(cols)] for i in range(rows)]

        else:
            buttons.extend([[KeyboardButton(text=text)] for text in data])

    buttons.append([KeyboardButton(text='Отменить')]) if cancel_btn else buttons

    buttons.append([KeyboardButton(text='Панель администратора')]) if admin_status else buttons

    markup = ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)
    return markup



