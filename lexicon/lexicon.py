MAIN_MENU_LEXICON = {

    'main_menu': 'Вы попали в главное меню'
}

ADMIN_LEXICON = {

    'admin': '/admin',

    'admin_true': '<b>Вы стали администратором</b>',

    'admin_false': '<b>Вы перестали быть администатором</b>',

    'on_admin_panel': 'Вы попали на панель администратора',

    'fill_question': 'Напишите вопрос',

    'fill_answer': 'Напишите ответ',

    'added_to_db': 'Добавлено в базу данных',

    'fill_service': 'Напишите название услуги',

    'fill_service_answer': 'Напишите описание услуги',

    'fill_doctor': 'Нажмите на врача',

    'fill_department': 'Нажмите на отделение',

    'doctor_is_not_exist': 'Такого врача нет в базе данных, введите ещё раз',

    'fill_time': 'Введите новое время в формате HH:mm',

    'wrong_time': 'Введено некорректное время, введите еще раз\n'
                  'Пример: 11:30',

    'slot_added': 'Слот {} удачно добавлен к {}',

    'slot_already_added': 'Этот слот уже был добавлен',

    'delete_slot_process': 'Для удаления нажмите на нужный слот',

    'slot_removed': 'Слот {} удален',

    'choose_appointment': 'Выберите запись для редактирования',

    'no_appointments': 'Записей нет',

    'appointment_info':
            '<b>Информация о записи:</b>\n\n'
            'Отделение {}\n'
            'Врач {}\n'
            'Дата {}\n'
            'Время {}\n'
            'ФИО пациента {}\n'


}

ADMIN_KB_LEXICON = {

    'add_faq': 'Добавить FAQ',
    'add_service': 'Добавить услугу',
    'add_new_slot': 'Добавить слот у врача',
    'delete_doctors_slot': 'Удалить слот у врача',
    'edit_appointment': 'Редактирование записей к врачу',
}


MAIN_KB_LEXICON = {

    'faq': '❓ Часто задаваемые вопросы',
    'clinic_schedule': '🕒 Расписание работы клиники',
    'appointment': '📝 Запись к врачу',
    'call_request': '📩 Заявка на звонок',
    'contact_information': '📱 Контактная информация',
    'services': '📂 Услуги',
}


CALL_REQUEST_LEXICON = {

    'fill_name': 'Оформление заявки на звонок\n'
                 'Напишите свое ФИО',

    'fill_problem': 'Опишите свою проблему',

    'fill_phone_number': 'Оставьте свой номер телефона',

    'request_accepted': 'Спасибо! Ваша заявка принята, мы обязательно позвоним вам!'

}

APPOINTMENT_LEXICON = {
    'choose_department': 'Выберите отделение',
    'choose_doctor': 'Выберите врача',
    'choose_date': 'Выберите дату',
    'choose_time': 'Вы выбрали {}, теперь нужно выбрать время:',
    'fill_name': 'Введите ФИО пациента',
    'fill_phone_number': 'Введите свой номер телефона',
    'no_free_slots': 'К этому врачу нет записи, вы можете выбрать другого',
    'success': '{}, вы записаны {} в {} часов к {}',
    'success_update': 'Запись обновлена'

}

FAQ_LEXICON = {

    'choose_faq': 'Выберите интересующий вас вопрос',
}

SERVICES_LEXICON = {

    'choose_service': 'Выберите интересующую вас услугу'
}

START_COMMAND = {

    'info': '<b>Здравствуйте!</b>\n'
            '<b>Вас приветствует помощник медицинского центра!</b>\n'

}

CLINIC_SCHEDULE = {

    'info': '<b>Время работы:</b>\n\n'
            'Пн-Пт. с 7-00 до 20-00 \n'
            'Сб. с 8-00 до 20-00\n'
            'Вс. с 8-00 до 17-00',
}

CONTACT_INFORMATION = {

    'info': '<b>Наши контакты:</b>\n'
            'Регистратура - +7 993 435 8898\n'
            'Почта - MedicalCenter@yandex.ru',
}
