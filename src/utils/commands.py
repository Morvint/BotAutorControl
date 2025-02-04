from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeDefault

async def set_commands(bot: Bot):
    commands = [
        BotCommand(command='start', description='Запускаем бота'),
        BotCommand(command='help', description='Помощь в работе с ботом (пока в разработке)'),
        BotCommand(command='request', description='Начинает процедуру создания вопроса'),
        BotCommand(command='check_wait_reg', description='Проверяет, сколько пользователей ожидают подтверждение регистрации'),
        BotCommand(command='table', description='Отправляет таблицу с вопросами')
    ]

    await bot.delete_my_commands()
    await bot.set_my_commands(commands, BotCommandScopeDefault())