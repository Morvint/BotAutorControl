from aiogram import Bot
from aiogram.types import Message

from src.keyboards.register_kb import register_keyboard

async def get_start(message: Message, bot: Bot):
    await bot.send_message(message.from_user.id, text=f'Здраствуйте. Вас приветствует бот авторского надзора компании ГлавСтрой',
                                                    reply_markup=register_keyboard)