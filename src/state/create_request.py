from aiogram.fsm.state import StatesGroup, State

class requestState(StatesGroup):
    objec = State()
    block = State()
    korpus = State()
    company = State()
    paragraph = State()
    numberlist = State()
    question = State()
    photo = State()
    withphoto = State()