from aiogram import Bot
from aiogram.types import BotCommand


async def set_default_commands(bot: Bot):
    commands = [
            BotCommand(command="chapters", description="Перейти к разделам"),
            BotCommand(command="help", description="Справочная информация"),
        ]
    await bot.set_my_commands(commands=commands)


async def on_startup(bot: Bot):
    # await set_default_commands(bot=bot)
    print("bot started")


async def on_shutdown(bot: Bot):
    await bot.delete_my_commands()
    print("bot shutdown")
