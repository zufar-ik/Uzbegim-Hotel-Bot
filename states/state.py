from aiogram.dispatcher.filters.state import StatesGroup, State


class Reklama(StatesGroup):
    reklama = State()
    reklama_2 = State()
    reklama_3 = State()
    reklama_4 = State()
    reklama_5 = State()
    reklama_6 = State()
    reklama_7 = State()


class Send(StatesGroup):
    up = State()
    down = State()


class Payments(StatesGroup):
    peyments = State()
    back = State()

class Admin(StatesGroup):
    ww = State()
    first = State()
    second = State()
    third = State()
    fourth = State()