import os
import re
import datetime

from aiogram import Bot
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.enums.parse_mode import ParseMode

from src.state.create_request import requestState
from src.keyboards.request_kb import objec_kb, block_kb, korpus_kb, photo_kb
from src.utils.database import Database

async def create_request(message: Message, state: FSMContext, bot: Bot):
    await bot.send_message(message.from_user.id, f'Выберете объект', reply_markup=objec_kb())
    await state.set_state(requestState.objec)

async def select_objec(callback: CallbackQuery, state: FSMContext):
    await state.update_data(objec=callback.data)
    request_data = await state.get_data()
    req_object = request_data.get('objec')
    await callback.message.edit_reply_markup(reply_markup=None)
    await callback.message.edit_text(text=f'Обект выбран')
    await callback.message.answer(text=f'Выберете квартал', reply_markup=block_kb(req_object))
    await callback.answer()
    await state.set_state(requestState.block)

async def select_block(callback: CallbackQuery, state: FSMContext):
    await state.update_data(block=callback.data)
    request_data = await state.get_data()
    req_block = request_data.get('block')
    await callback.message.edit_reply_markup(reply_markup=None)
    await callback.message.edit_text(text=f'Квартал выбран')
    await callback.message.answer(text=f'Выберете корпус', reply_markup=korpus_kb(req_block))
    await callback.answer()
    await state.set_state(requestState.korpus)

async def select_korpus(callback: CallbackQuery, state: FSMContext):
    await state.update_data(korpus=callback.data)
    await callback.message.edit_reply_markup(reply_markup=None)
    await callback.message.edit_text(text=f'Корпус выбран')
    await callback.message.answer(text=f'Введите название раздела документации')
    await callback.answer()
    await state.set_state(requestState.paragraph)

async def select_paragraph(message: Message, state: FSMContext, bot: Bot):
    db = Database(os.getenv('DATABASE_NAME'))
    user = db.select_user_id(message.from_user.id)
    await state.update_data(paragraph=message.text)
    await state.update_data(fullname=user[1])
    await bot.send_message(message.from_user.id, text=f'Введите номер листа')
    await state.set_state(requestState.numberlist)

async def select_numberlist(message: Message, state: FSMContext, bot: Bot):
    if (re.findall(r'^\d+$', message.text)):
        await state.update_data(numberlist=message.text)
        await bot.send_message(message.from_user.id, text=f'Напишете ваш вопрос')
        await state.set_state(requestState.question)
    else:
        await bot.send_message(message.from_user.id, text=f'Номер листа должен содержать только цифры')

async def select_question(message: Message, state: FSMContext, bot: Bot):
    await state.update_data(question=message.text)
    await bot.send_message(message.from_user.id, text=f'Можете приложить фотографию для пояснения вопроса?', reply_markup=photo_kb())
    await state.set_state(requestState.photo)

async def select_photo(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_reply_markup(reply_markup=None)
    if callback.data == 'Да':
        await callback.message.answer(f'Приложите фотографию')
        await callback.answer()
        await state.set_state(requestState.withphoto)
    else:
        db = Database(os.getenv('DATABASE_NAME'))
        request_data = await state.get_data()
        req_object = request_data.get('objec')
        req_block = request_data.get('block')
        req_korpus = request_data.get('korpus')
        req_name = request_data.get('fullname')
        req_paragraph = request_data.get('paragraph')
        req_numberlist = request_data.get('numberlist')
        req_question = request_data.get('question')
        req_photo = None
        req_date_question = datetime.date.today()
        db.add_question_no_photo(req_block, req_korpus, req_name, req_paragraph, req_numberlist, req_question, req_photo, req_date_question)
        msg = (f'<b>Данные запроса</b>\n\n' +
            f'<b>Объект:</b> {req_object}\n' +
            f'<b>Квартал:</b> {req_block}\n' +
            f'<b>Корпус:</b> {req_korpus}\n' +
            f'<b>Вас зовут:</b> {req_name}\n' +
            f'<b>Название раздела:</b> {req_paragraph}\n' +
            f'<b>Номер листа:</b> {req_numberlist}\n' +
            f'<b>Вопрос:</b> {req_question}\n')
        await callback.message.answer(text='Спасибо, ваш запрос зарегестрирован')
        await callback.message.answer(text=msg, parse_mode=ParseMode.HTML)
        await callback.message.answer(text='Вы можете уточнить статус решения вашей проблемы на ближайшем дне авторского надзора')
        await state.clear()

async def answer_with_photo(message: Message, state: FSMContext, bot: Bot):
    db = Database(os.getenv('DATABASE_NAME'))
    await state.update_data(id_photo=message.photo[-1].file_id)
    request_data = await state.get_data()
    req_object = request_data.get('objec')
    req_block = request_data.get('block')
    req_korpus = request_data.get('korpus')
    req_name = request_data.get('fullname')
    req_paragraph = request_data.get('paragraph')
    req_numberlist = request_data.get('numberlist')
    req_question = request_data.get('question')
    req_photo = request_data.get('id_photo')
    req_date_question = datetime.date.today()
    db.add_question_no_photo(req_block, req_korpus, req_name, req_paragraph, req_numberlist, req_question, req_photo, req_date_question)
    msg = (f'<b>Данные запроса</b>\n\n' +
           f'<b>Объект:</b> {req_object}\n' +
           f'<b>Квартал:</b> {req_block}\n' +
           f'<b>Корпус:</b> {req_korpus}\n' +
           f'<b>Вас зовут:</b> {req_name}\n' +
           f'<b>Название раздела:</b> {req_paragraph}\n' +
           f'<b>Номер листа:</b> {req_numberlist}\n' +
           f'<b>Вопрос:</b> {req_question}\n')
    await bot.send_message(message.from_user.id, text='Спасибо, ваш запрос зарегестрирован')
    await bot.send_message(message.from_user.id, text=msg, parse_mode=ParseMode.HTML)
    await bot.send_message(message.from_user.id, text='Вы можете уточнить статус решения вашей проблемы на ближайшем дне авторского надзора')
    await state.clear()