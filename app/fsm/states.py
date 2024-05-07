from aiogram.filters.state import State, StatesGroup


class PreButtonStates(StatesGroup):
    chapter_selected = State()
    cipher_selected = State()


class ButtonsStates(StatesGroup):
    button1 = State()
    button2 = State()
