from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from lexicon.lexicon import MAIN_MENU_LEXICON


def build_menu_keyboard(admin_status):

    faq_btn = KeyboardButton(
        text=MAIN_MENU_LEXICON['faq'],

    )

    clinic_schedule_btn = KeyboardButton(
        text=MAIN_MENU_LEXICON['clinic_schedule'],

    )

    appointment_btn = KeyboardButton(
        text=MAIN_MENU_LEXICON['appointment'],

    )

    call_request_btn = KeyboardButton(
        text=MAIN_MENU_LEXICON['call_request'],
    )

    contact_information_btn = KeyboardButton(
        text=MAIN_MENU_LEXICON['contact_information'],
    )

    services_btn = KeyboardButton(
        text=MAIN_MENU_LEXICON['services'],
    )

    admin_panel_btn = KeyboardButton(
        text=MAIN_MENU_LEXICON['admin_panel'],
    )

    rows = [
        [faq_btn, appointment_btn],
        [clinic_schedule_btn, contact_information_btn],
        [call_request_btn, services_btn]
    ]

    if admin_status:
        rows.append([admin_panel_btn])

    markup = ReplyKeyboardMarkup(keyboard=rows)

    return markup


