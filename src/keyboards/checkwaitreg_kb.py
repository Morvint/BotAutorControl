from aiogram.utils.keyboard import InlineKeyboardBuilder

yes_no = ['Да', 'Нет']

def confirm_kb():
    kb = InlineKeyboardBuilder()
    for value in yes_no:
        kb.button(text=f'{value}', callback_data=f'{value}')
    return kb.adjust(2).as_markup()