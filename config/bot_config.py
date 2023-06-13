import logging
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from dotenv import dotenv_values

config = dotenv_values('./config/.env')
API_TOKEN = config['API_TOKEN']
ADMIN = int(config['ADMIN'])

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())