from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def build_menu_keyboard():

    faq_btn = KeyboardButton(
        text='Часто задаваемые вопросы',

    )

    clinic_schedule_btn = KeyboardButton(
        text='Расписание работы клиники',

    )

    appointment_btn = KeyboardButton(
        text='Запись к врачу',

    )


    call_request_btn = KeyboardButton(
        text='Заявка на звонок',
    )


    contact_information_btn = KeyboardButton(
        text='Контактная информация',
    )

    services_btn = KeyboardButton(
        text='Услуги',
    )

    admin_panel_btn = KeyboardButton(
        text='Панель администратора',
    )

    rows = [
        [faq_btn, appointment_btn],
        [clinic_schedule_btn, contact_information_btn],
        [call_request_btn, services_btn],
        [admin_panel_btn]
    ]

    markup = ReplyKeyboardMarkup(keyboard=rows)

    return markup


