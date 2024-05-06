from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from lexicon.lexicon import MAIN_MENU_LEXICON
from lexicon.lexicon import ADMIN_LEXICON


def build_admin_keyboard():

    faq_btn = KeyboardButton(
        text=ADMIN_LEXICON['add_faq']
    )

    service_btn = KeyboardButton(
        text=ADMIN_LEXICON['add_service']
    )

    back_btn = KeyboardButton(
        text=MAIN_MENU_LEXICON['back']
    )

    rows = [
        [faq_btn],
        [service_btn],
        [back_btn]
    ]

    markup = ReplyKeyboardMarkup(keyboard=rows)

    return markup

