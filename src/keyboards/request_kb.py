from aiogram.utils.keyboard import InlineKeyboardBuilder

objects = ['Юнтолово']
blocks = {'Юнтолово': ['Квартал 31', 'Квартал 34', 'Квартал 35']}
korpuses ={'Квартал 31': ['Корпус 1', 'Корпус 2'],
           'Квартал 34': ['Корпус 1', 'Корпус 2'],
           'Квартал 35': ['Корпус 1', 'Корпус 2', 'Корпус 3']}
yes_no = ['Да', 'Нет']

def objec_kb():
    kb = InlineKeyboardBuilder()
    for obj in objects:
        kb.button(text=f'{obj}', callback_data=f'{obj}')
    return kb.adjust(1).as_markup()

def block_kb(key):
    kb = InlineKeyboardBuilder()
    for i, block in enumerate(blocks[key]):
        kb.button(text=f'{block}', callback_data=f'{block}')
    return kb.adjust(1).as_markup()

def korpus_kb(key):
    kb = InlineKeyboardBuilder()
    for i, korpus in enumerate(korpuses[key]):
        kb.button(text=f'{korpus}', callback_data=f'{korpus}')
    return kb.adjust(1).as_markup()

def photo_kb():
    kb = InlineKeyboardBuilder()
    for value in yes_no:
        kb.button(text=f'{value}', callback_data=f'{value}')
    return kb.adjust(2).as_markup()