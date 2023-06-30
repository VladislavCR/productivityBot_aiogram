from aiogram import types
from aiogram.dispatcher import FSMContext

from config.bot_config import bot, dp
from keyboards.admin_kb import (admin_kb_main_menu,
                                admin_kb_choices_menu,
                                admin_kb_add_shop,
                                admin_kb_cr,
                                admin_kb_mo,
                                admin_kb_sin,
                                admin_kb_re,
                                admin_kb_xc)
from keyboards.director_kb import director_kb_main_menu
from keyboards.employee_kb import (employee_kb_registration,
                                   employee_registed_kb)
from database.user_role.check_role import check_bd_user_role


@dp.message_handler(commands=['start'])
async def start_cmd(message: types.Message):
    user_id = int(message.from_user.id)
    check_user_role = await check_bd_user_role(user_id=user_id)
    await bot.delete_message(chat_id=message.from_user.id,
                             message_id=message.message_id)
    if check_user_role == 'admin':
        await bot.send_message(chat_id=message.from_user.id,
                               text='Привет! Админ',
                               reply_markup=admin_kb_choices_menu)
    elif check_user_role == 'director':
        await bot.send_message(chat_id=message.from_user.id,
                               text='Привет! Директор',
                               reply_markup=director_kb_main_menu)
    elif check_user_role == 'employee':
        await bot.send_message(chat_id=message.from_user.id,
                               text=f"Добро пожаловать, "
                               f"{message.from_user.first_name} "
                               f"{message.from_user.last_name}",
                               reply_markup=employee_registed_kb)
    else:
        await bot.send_message(chat_id=message.from_user.id,
                               text='Добро пожаловать! Давай зарегистрируемся',
                               reply_markup=employee_kb_registration)


@dp.message_handler(commands=["cancel"], state="*")
async def cancel_cmd(message: types.Message, state: FSMContext):
    curr_state = await state.get_state()
    if curr_state is None:
        return
    else:
        await state.finish()
        await bot.delete_message(chat_id=message.from_user.id,
                                 message_id=message.message_id)
        await message.reply('Вы прервали операцию',
                            reply_markup=admin_kb_main_menu)


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
                           text='Добавить магазин в бренд CR!',
                           reply_markup=admin_kb_cr)


@dp.callback_query_handler(text="add_SIN")
async def new_shop_sin(callback_query: types.CallbackQuery):
    await bot.delete_message(chat_id=callback_query.from_user.id,
                             message_id=callback_query.message.message_id)
    await bot.send_message(chat_id=callback_query.from_user.id,
                           text='Добавить магазин в бренд SIN!',
                           reply_markup=admin_kb_sin)


@dp.callback_query_handler(text="add_RE")
async def new_shop_re(callback_query: types.CallbackQuery):
    await bot.delete_message(chat_id=callback_query.from_user.id,
                             message_id=callback_query.message.message_id)
    await bot.send_message(chat_id=callback_query.from_user.id,
                           text='Добавить магазин в бренд RE!',
                           reply_markup=admin_kb_re)


@dp.callback_query_handler(text="add_MO")
async def new_shop_mo(callback_query: types.CallbackQuery):
    await bot.delete_message(chat_id=callback_query.from_user.id,
                             message_id=callback_query.message.message_id)
    await bot.send_message(chat_id=callback_query.from_user.id,
                           text='Добавить магазин в бренд MO!',
                           reply_markup=admin_kb_mo)


@dp.callback_query_handler(text="add_XC")
async def new_shop_xc(callback_query: types.CallbackQuery):
    await bot.delete_message(chat_id=callback_query.from_user.id,
                             message_id=callback_query.message.message_id)
    await bot.send_message(chat_id=callback_query.from_user.id,
                           text='Добавить магазин в бренд!',
                           reply_markup=admin_kb_xc)


@dp.callback_query_handler(text="go_back_main_menu")
async def view_users(callback_query: types.CallbackQuery):
    await bot.delete_message(chat_id=callback_query.from_user.id,
                             message_id=callback_query.message.message_id)
    await bot.send_message(chat_id=callback_query.from_user.id,
                           text="Главное меню!",
                           reply_markup=admin_kb_main_menu)
