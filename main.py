from aiogram import types, executor
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher import FSMContext

from config.bot_config import bot, dp
from keyboards.inline_keyboards import (admin_panel_main_menu,
                                        director_panel_main_menu,
                                        staff_pannel_main_menu)
from database.user_role.check_user_role import check_bd_user_role


@dp.message_handler(commands=['cancel'], state='*')
async def cancel_cmd(message: types.Message, state: FSMContext):
    if state is None:
        return
    await state.finish()
    await message.reply('Вы прервали операцию',
                        reply_markup=admin_panel_main_menu)


@dp.message_handler(commands=['start'])
async def start_cmd(message: types.Message):
    user_id = int(message.from_user.id)
    check_user_role = await check_bd_user_role(id=user_id)
    if check_user_role == 'admin':
        await bot.send_message(chat_id=message.from_user.id,
                               text='Привет! Админ',
                               reply_markup=admin_panel_main_menu)
    elif check_user_role == 'director':
        await bot.send_message(chat_id=message.from_user.id,
                               text='Привет! Директор',
                               reply_markup=director_panel_main_menu)
    else:
        await bot.send_message(chat_id=message.from_user.id,
                               text='Привет! Сотрудник',
                               reply_markup=staff_pannel_main_menu)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
