from aiogram.types import BotCommand, BotCommandScopeDefault
from app.bot.bot import bot

commands = [
    BotCommand(command="start", description="Начать работу с ботом"),
    BotCommand(command="add_account", description="Добавить аккаунт"),
    BotCommand(command="my_accounts", description="Мои аккаунты")
]

async def set_bot_commands(bot):
    await bot.set_my_commands(
        commands,
        scope=BotCommandScopeDefault()
    )
