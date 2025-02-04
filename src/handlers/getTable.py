import os

from aiogram import Bot
from aiogram.types import Message
# from aiogram.types import InputFile
from aiogram.types import FSInputFile

from src.utils.database import Database

async def get_table(message: Message, bot: Bot):
    db = Database(os.getenv('DATABASE_NAME'))
    db.get_questions_table()
    await bot.send_document(message.from_user.id, FSInputFile('table.xlsx'), caption='Таблица с вопросами:')