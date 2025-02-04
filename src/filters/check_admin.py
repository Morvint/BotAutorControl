import os

from aiogram.filters import BaseFilter
from aiogram.types import Message

from src.utils.database import Database

class CheckAdmin(BaseFilter):
    async def __call__(self, message: Message):
        try:
            admin_id = os.getenv('ADMIN_ID')
            db = Database(os.getenv('DATABASE_NAME'))
            users = db.select_user_id(message.from_user.id)
            return users[3] in admin_id
            # return True
        except:
            return False