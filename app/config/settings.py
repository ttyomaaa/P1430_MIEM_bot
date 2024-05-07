import os

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.utils.chat_action import ChatActionMiddleware
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_TOKEN = os.getenv('TOKEN')

storage = MemoryStorage()
bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher(bot=bot, storage=storage)
dp.message.middleware(ChatActionMiddleware())
