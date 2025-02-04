import os

from aiogram.filters import BaseFilter
from aiogram.types import Message

from src.utils.database import Database

class CheckRegUser(BaseFilter):
    async def __call__(self, message: Message):
        try:
            db = Database(os.getenv('DATABASE_NAME'))
            users = db.select_wait_reg_user_id(message.from_user.id)
            if (users):
                return True
            else:
                return False
        except:
            return False