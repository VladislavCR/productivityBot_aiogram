from aiogram import types
from config.bot_config import bot, dp
from keyboards.admin_kb import *
from admin_panel.admin_fsm import *


@dp.callback_query_handler(text="add_shop")
async def new_shop(callback_query: types.CallbackQuery):
    await bot.delete_message(chat_id=callback_query.from_user.id,
                             message_id=callback_query.message.message_id)
    await bot.send_message(chat_id=callback_query.from_user.id,
                           text='Выбери бренд!',
                           reply_markup=admin_kb_add_shop)


@dp.callback_query_handler(text="add_CR")
async def new_shop_cr(callback_query: types.CallbackQuery):
    await bot.delete_message(chat_id=callback_query.from_user.id,
                             message_id=callback_query.message.message_id)
    await bot.send_message(chat_id=callback_query.from_user.id,
                           text='Выбери бренд!',
                           reply_markup=admin_kb_cr)


@dp.callback_query_handler(text="add_SIN")
async def new_shop_sin(callback_query: types.CallbackQuery):
    await bot.delete_message(chat_id=callback_query.from_user.id,
                             message_id=callback_query.message.message_id)
    await bot.send_message(chat_id=callback_query.from_user.id,
                           text='Выбери бренд!',
                           reply_markup=admin_kb_sin)


@dp.callback_query_handler(text="add_RE")
async def new_shop_re(callback_query: types.CallbackQuery):
    await bot.delete_message(chat_id=callback_query.from_user.id,
                             message_id=callback_query.message.message_id)
    await bot.send_message(chat_id=callback_query.from_user.id,
                           text='Выбери бренд!',
                           reply_markup=admin_kb_re)


@dp.callback_query_handler(text="add_MO")
async def new_shop_mo(callback_query: types.CallbackQuery):
    await bot.delete_message(chat_id=callback_query.from_user.id,
                             message_id=callback_query.message.message_id)
    await bot.send_message(chat_id=callback_query.from_user.id,
                           text='Выбери бренд!',
                           reply_markup=admin_kb_mo)


@dp.callback_query_handler(text="add_XC")
async def new_shop_xc(callback_query: types.CallbackQuery):
    await bot.delete_message(chat_id=callback_query.from_user.id,
                             message_id=callback_query.message.message_id)
    await bot.send_message(chat_id=callback_query.from_user.id,
                           text='Выбери бренд!',
                           reply_markup=admin_kb_xc)