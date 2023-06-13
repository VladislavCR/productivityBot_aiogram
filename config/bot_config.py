import logging
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from dotenv import dotenv_values
from pathlib import Path


# Путь к папке config
BASE_DIR = Path(__file__).resolve().parent.parent
CONFIG_DIR = BASE_DIR.joinpath('config')


# Получение токена из файла .env
config = dotenv_values(CONFIG_DIR/'.env')
API_TOKEN = config['API_TOKEN']

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())
