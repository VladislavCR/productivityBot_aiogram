from aiogram import types
from config.bot_config import dp, bot
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from keyboards.employee_kb import (employee_kb_registration,
                                   employee_kb_return,
                                   employee_registed_kb)
from keyboards.reply_kb import choice_position_kb
from database.users.create_user import create_user_bd
from database.shops.check_shop import check_shop
from database.user_role.create_role import create_user


class FSM_create_new_user(StatesGroup):
    first_name = State()
    last_name = State()
    user_position = State()
    shop_id = State()


@dp.callback_query_handler(text="start_reg", state=None)
async def start_registration(callback_query: types.CallbackQuery):
    await FSM_create_new_user.first_name.set()
    await bot.delete_message(chat_id=callback_query.from_user.id,
                             message_id=callback_query.message.message_id)
    await bot.send_message(chat_id=callback_query.from_user.id,
                           text="Начало регистрации!\n"
                           "Введи свое имя:",
                           reply_markup=employee_kb_return)


@dp.message_handler(state=FSM_create_new_user.first_name)
async def create_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        test_text = isinstance(message.text, str)
        if test_text:
            data['first_name'] = message.text
            await FSM_create_new_user.next()
            await bot.send_message(chat_id=message.from_user.id,
                                   text=f"Имя: {message.text}\n"
                                   "Введите свою фамилию",
                                   reply_markup=employee_kb_return)
        else:
            await state.finish()
            await bot.send_message(chat_id=message.from_user.id,
                                   text=f"\nОшибка вы прислали не строку\n"
                                   f"Имя пользователя:  {message.text}\n"
                                   f"\nПопробуйте ещё раз",
                                   reply_markup=employee_kb_registration)


@dp.message_handler(state=FSM_create_new_user.last_name)
async def create_female(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        test_text = isinstance(message.text, str)
        if test_text:
            data['last_name'] = message.text
            await FSM_create_new_user.next()
            await bot.send_message(chat_id=message.from_user.id,
                                   text=f"Фамилия: {message.text}\n"
                                   "Выбери свою должность",
                                   reply_markup=choice_position_kb)
        else:
            await state.finish()
            await bot.send_message(chat_id=message.from_user.id,
                                   text=f"\nОшибка вы прислали не строку\n"
                                   f"Фамилия пользователя:  {message.text}\n"
                                   f"\nПопробуйте ещё раз",
                                   reply_markup=employee_kb_registration)


@dp.message_handler(state=FSM_create_new_user.user_position)
async def create_position(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        test_text = isinstance(message.text, str)
        if test_text:
            data['user_position'] = message.text
            await FSM_create_new_user.next()
            await bot.send_message(chat_id=message.from_user.id,
                                   text=f"Твоя должность: {message.text}\n"
                                   "Напиши номер своего магазина",
                                   reply_markup=employee_kb_return)
        else:
            await state.finish()
            await bot.send_message(chat_id=message.from_user.id,
                                   text=f"\nОшибка вы прислали не строку\n"
                                   f"Твоя должость:  {message.text}\n"
                                   f"\nПопробуйте ещё раз",
                                   reply_markup=employee_kb_registration,
                                   )


@dp.message_handler(state=FSM_create_new_user.shop_id)
async def choice_shop(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        test_shop = str.isdigit(message.text)
        if test_shop:
            try:
                check_bd = await check_shop(shop_number=int(message.text))
                if check_bd:
                    async with state.proxy() as data:
                        data['shop_id'] = int(message.text)
                        await state.finish()
                        await create_user_bd(user_id=message.from_user.id,
                                             first_name=data['first_name'],
                                             last_name=data['last_name'],
                                             user_position=data['user_position'],
                                             shop_id=data['shop_id'])
                        await create_user(user_id=message.from_user.id)
                        await bot.send_message(chat_id=message.from_user.id,
                                               text=f"\nВы зарегистрированы\n"
                                               f"ID пользователя:  {message.from_user.id}\n"
                                               f"ФИО пользователя:  {data['first_name']} {data['last_name']}\n"
                                               f"Должность пользователя:  {data['user_position']}\n"
                                               f"Ваш магазин: {data['shop_id']}",
                                               reply_markup=employee_registed_kb)
                else:
                    await state.finish()
                    await bot.send_message(chat_id=message.from_user.id,
                                           text=f"\nОшибка, такого номера магазина нет в базе\n"
                                           f"Номер магазина:  {message.text}\n"
                                           f"\nПопробуйте ещё раз",
                                           reply_markup=employee_kb_registration)
            except ValueError:
                await state.finish()
                await bot.send_message(chat_id=message.from_user.id,
                                       text=f"\nОшибка ID пользователя (Это не число)\n"
                                       f"ID пользователя:  {message.text}\n"
                                       f"\nПопробуйте снова",
                                       reply_markup=employee_kb_registration)
