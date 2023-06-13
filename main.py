from aiogram import types, executor
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher import FSMContext

from config.bot_config import bot, dp, ADMIN
from keyboards.inline_keyboards import (admin_panel_main_menu,
                                        director_panel_main_menu,
                                        staff_pannel_main_menu)



class ProfileStatesGroup(StatesGroup):
    photo = State()
    name = State()
    age = State()
    description = State()


@dp.message_handler(commands=['cancel'], state='*')
async def cancel_cmd(message: types.Message, state: FSMContext):
    if state is None:
        return
    await state.finish()
    await message.reply('Вы прервали операцию',
                        reply_markup=admin_panel_main_menu)


@dp.message_handler(commands=['start'])
async def start_cmd(message: types.Message):
    await message.answer('Привет!', reply_markup=admin_panel_main_menu)


@dp.message_handler(commands=['director'])
async def director_cmd(message: types.Message, state: FSMContext):
    await message.answer('Директор', reply_markup=director_panel_main_menu)


@dp.message_handler(commands=['staff'])
async def staff_cmd(message: types.Message, state: FSMContext):
    await message.answer('Сотрудник', reply_markup=staff_pannel_main_menu)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
