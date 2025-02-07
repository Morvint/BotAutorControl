import re
import os

from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext

from src.state.register import RegisterState
from src.utils.database import Database

async def start_register(message: Message, state: FSMContext):
    db = Database(os.getenv('DATABASE_NAME'))
    users_reg = db.select_user_id(message.from_user.id)
    users_wait_reg = db.select_wait_reg_user_id(message.from_user.id)
    if(users_reg):
        await message.answer(f'{users_reg[1]}\nВы уже зарегестрированы', reply_markup=ReplyKeyboardRemove())
    elif(users_wait_reg):
        await message.answer(f'{users_wait_reg[1]}\nВы уже отправили запрос на регистрацию', reply_markup=ReplyKeyboardRemove())
    else:
        await message.answer(text=f'Давайте начнем регистрацию\nДля начала введите ваше имя', reply_markup=ReplyKeyboardRemove())
        await state.set_state(RegisterState.regName)

async def register_name(message: Message, state: FSMContext):
    await message.answer(f'{message.text}, укажите номер телефона\nФормат телефона: 8ххххххххх или +7ххххххххх')
    await state.update_data(regname=message.text)
    await state.set_state(RegisterState.regPhone)

async def register_phone(message: Message, state: FSMContext):
    if (re.findall(r'^(8|\+7)\d{10}$', message.text)):
        await state.update_data(regphone=message.text)
        reg_data = await state.get_data()
        reg_name = reg_data.get('regname')
        reg_phone = reg_data.get('regphone')
        msg = f'Приятно познакомиться, {reg_name}\nВаш телефон: {reg_phone}\nПожалуйста, ожидайте, когда вашу регистрацию подвердят'
        await message.answer(text=msg)
        db = Database(os.getenv('DATABASE_NAME'))
        db.add_user_wait_reg(reg_name, reg_phone, message.from_user.id)
        await state.clear()
    else:
        await message.answer(f'Номер указан в неправильном формате.\n' +
                             f'Пожалуйста, укажите номер в правильном формате' +
                             '\nНапоминаю, верным форматом является: 8ххххххххх или +7ххххххххх')
    