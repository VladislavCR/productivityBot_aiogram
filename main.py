from aiogram import types, executor

from config.bot_config import bot, dp, ADMIN
from keyboards.keyboards import admin_panel_main_menu


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    user_id = message.from_user.id
    if user_id == ADMIN:
        await bot.send_message(chat_id=message.from_user.id,
                               text=f'Ваш ID: {message.from_user.id}',
                               reply_markup=admin_panel_main_menu)
    else:
        await bot.send_message(chat_id=message.from_user.id,
                               text=f'Ваш ID: {message.from_user.id}')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
