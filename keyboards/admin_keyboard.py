from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def build_admin_keyboard():

    faq_btn = KeyboardButton(
        text='Добавить FAQ',
    )

    back_btn = KeyboardButton(
        text='Назад',
    )

    rows = [
        [faq_btn],
        [back_btn]
    ]

    markup = ReplyKeyboardMarkup(keyboard=rows)

    return markup

