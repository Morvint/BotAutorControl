import os

from aiogram import Bot
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from src.state.check_wait_reg import stateCheckWaitReg
from src.keyboards.checkwaitreg_kb import confirm_kb
from src.utils.database import Database

# Добавить в базу данных запрос для уточнения количества 
async def check_wait_reg(message: Message, state: FSMContext, bot: Bot):
    db = Database(os.getenv('DATABASE_NAME'))
    cout_wait_reg = db.count_wait_reg()
    user = db.first_wait_reg_user()
    if cout_wait_reg > 0:
        await bot.send_message(message.from_user.id, f'Количество пользователей, ожидающих регистрации: {cout_wait_reg}\n' +
                            f'ФИО: {user[1]}\nНомер телефона: {user[2]}\n' +
                            f'Хотите, что бы он мог пользоваться ботом?', reply_markup=confirm_kb())
        await state.set_state(stateCheckWaitReg.confirm)
    else:
        await bot.send_message(message.from_user.id, text=f'Количество пользователей, ожидающих регистрации: {cout_wait_reg}\n')

async def select_confirm(callback: CallbackQuery, state: FSMContext, bot: Bot):
    await state.update_data(confirm=callback.data)
    dat = await state.get_data()
    confirm_dat = dat.get('confirm')
    db = Database(os.getenv('DATABASE_NAME'))
    user = db.first_wait_reg_user()
    count = db.count_wait_reg()
    if (confirm_dat == 'Да' and count != 0):
        await bot.send_message(user[3], f'Поздравляю! Вы успешно зарегистрировались!')
        db.add_user(user[1], user[2], user[3])
        db.del_user_wait_reg(user[3])
        cout_wait_reg = db.count_wait_reg()
        user = db.first_wait_reg_user()
        await callback.message.edit_reply_markup(reply_markup=None)
        await callback.message.edit_text(text=f'Пользователь добавлен')
        if cout_wait_reg != 0:
            await callback.message.answer(text=f'Количество пользователей, ожидающих регистрации: {cout_wait_reg}\n' +
                                        f'ФИО: {user[1]}\nНомер телефона: {user[2]}\n' +
                                        f'Хотите, что бы он мог пользоваться ботом?', reply_markup=confirm_kb())
        await callback.answer()
    elif(confirm_dat == 'Нет' and count != 0):
        print(type(user[3]))
        db.del_user_wait_reg(user[3])
        cout_wait_reg = db.count_wait_reg()
        user = db.first_wait_reg_user()
        await callback.message.edit_reply_markup(reply_markup=None)
        await callback.message.edit_text(text=f'Пользователю отказано в регистрации')
        if cout_wait_reg != 0:
            await callback.message.answer(text=f'Количество пользователей, ожидающих регистрации: {cout_wait_reg}\n' +
                                        f'ФИО: {user[1]}\nНомер телефона: {user[2]}\n' +
                                        f'Хотите, что бы он мог пользоваться ботом?', reply_markup=confirm_kb())
        await callback.answer()
    else:
        db.del_user_wait_reg(user[3])
        cout_wait_reg = db.count_wait_reg()
        await callback.message.edit_reply_markup(reply_markup=None)
        await callback.message.edit_text(f'Количество пользователей, ожидающих регистрации: {cout_wait_reg}')
        await callback.answer()
        await state.clear()
