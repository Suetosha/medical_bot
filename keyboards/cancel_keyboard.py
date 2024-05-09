from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from lexicon.lexicon import MAIN_MENU_LEXICON


def build_cancel_keyboard():
    markup = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text=MAIN_MENU_LEXICON['cancel'])]], resize_keyboard=True)
    return markup