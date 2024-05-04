from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

def faq_kb(data):
    buttons = [[KeyboardButton(text=question)] for question in data]
    markup = ReplyKeyboardMarkup(keyboard=buttons)
    return markup
