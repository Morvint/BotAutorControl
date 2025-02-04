import asyncio
from dotenv import load_dotenv
import os
import logging

from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.enums.parse_mode import ParseMode

from src.utils.commands import set_commands
from src.handlers.start import get_start
from src.state.register import RegisterState
from src.state.create_request import requestState
from src.state.check_wait_reg import stateCheckWaitReg
from src.handlers import createRequest, register, getTable
from src.handlers.admin import checkWaitReg
from src.filters.check_admin import CheckAdmin
from src.filters.check_reg_user import CheckRegUser

load_dotenv()

token = os.getenv('TOKEN')
admin_id = os.getenv('ADMIN_ID')
superuser = os.getenv('SUPERUSER')

bot = Bot(token=token, parce_mode='HTML')
dp = Dispatcher()

async def start_bot(bot: Bot):
    await bot.send_message(superuser, text='<b>Бот запущен</b>', parse_mode=ParseMode.HTML)

#Регистрация команды стар и запуска бота
dp.startup.register(start_bot)
dp.message.register(get_start, Command(commands='start'))

#Регистация некоторых команд
dp.message.register(getTable.get_table, Command('table'), CheckAdmin())

#Регистрация хендлеров запроса на регистрацию регистрации (пока вносит в БД зарегистрированных)
dp.message.register(register.start_register, F.text == 'Зарегистистрироваться')
dp.message.register(register.register_name, RegisterState.regName)
dp.message.register(register.register_phone, RegisterState.regPhone)

#Регистрация хендлеров запроса
dp.message.register(createRequest.create_request, Command('request'), CheckRegUser())
dp.callback_query.register(createRequest.select_objec, requestState.objec)
dp.callback_query.register(createRequest.select_block, requestState.block)
dp.callback_query.register(createRequest.select_korpus, requestState.korpus)
dp.message.register(createRequest.select_paragraph, requestState.paragraph)
dp.message.register(createRequest.select_numberlist, requestState.numberlist)
dp.message.register(createRequest.select_question, requestState.question)
dp.callback_query.register(createRequest.select_photo, requestState.photo)
dp.message.register(createRequest.answer_with_photo, requestState.withphoto)

#Регистрация хендлеров подтверждений регистрации
dp.message.register(checkWaitReg.check_wait_reg, Command('check_wait_reg'), CheckAdmin())
dp.callback_query.register(checkWaitReg.select_confirm, stateCheckWaitReg.confirm)

async def start():
    await set_commands(bot)
    try:
        await bot.delete_webhook(drop_pending_updates=True) #Бот ингнориует сообщения, которые были написаны во время его отключения
        await dp.start_polling(bot)
    finally:
        await bot.session.close()

if __name__ =='__main__':
    try:
        logging.basicConfig(level=logging.INFO)
        asyncio.run(start())
    except KeyboardInterrupt:
        print('Exit')