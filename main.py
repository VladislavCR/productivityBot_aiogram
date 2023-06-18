from aiogram import executor

from config.bot_config import *
from admin_panel.admin_fsm import *
from admin_panel.callback_query import *
from admin_panel.directors_fsm import *
from admin_panel.employee_fsm import *

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
