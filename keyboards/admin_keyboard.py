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

    add_slot_btn = KeyboardButton(
        text=ADMIN_LEXICON['add_new_slot']
    )

    delete_slot_btn = KeyboardButton(
        text=ADMIN_LEXICON['delete_doctors_slot']
    )

    edit_appointment_btn = KeyboardButton(
        text=ADMIN_LEXICON['edit_appointment']
    )

    cancel_btn = KeyboardButton(
        text=MAIN_MENU_LEXICON['cancel']
    )

    rows = [
        [faq_btn],
        [service_btn],
        [add_slot_btn],
        [delete_slot_btn],
        [edit_appointment_btn],
        [cancel_btn]
    ]

    markup = ReplyKeyboardMarkup(keyboard=rows)

    return markup

