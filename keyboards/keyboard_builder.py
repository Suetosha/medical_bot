from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from lexicon.lexicon import MAIN_MENU_LEXICON


def kb_builder(data):
    buttons = [[KeyboardButton(text=text)] for text in data]
    markup = ReplyKeyboardMarkup(keyboard=buttons + [[KeyboardButton(text=MAIN_MENU_LEXICON['back'])]])
    return markup
