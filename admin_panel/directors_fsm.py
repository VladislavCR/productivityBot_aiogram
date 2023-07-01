from datetime import datetime
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import filters

from config.bot_config import bot, dp
from keyboards.director_kb import (director_kb_main_menu,
                                   director_kb_operations,
                                   director_kb_stop_productivitty)
from database.users.view_users import (get_employees,
                                       get_shop,
                                       get_employee_from_users)
from database.users.check_shop_user import check_shop_from_user
from database.users.delete_user import delete_user
from database.productivity.create_productivity import create_productivity
from database.productivity.check_avg_prod_shop import (
    check_avg_productivity_shops)
from database.productivity.check_avg_prod_users_in_shop import (
    check_avg_productivity_users_in_shop
)
from database.productivity.check_prod_by_day import (
    check_avg_productivity_by_day)
from admin_panel.callback_query import *


@dp.callback_query_handler(text="view_list")
async def view_list(callback_query: types.CallbackQuery):
    shop_id = await check_shop_from_user(callback_query.from_user.id)
    employees = await get_employees(shop_id=shop_id)
    n = 1
    text_message = ''
    try:
        for employee in employees:
            user_id = f"{employee['user_id']}"
            first_name = f"{employee['first_name']}"
            last_name = f"{employee['last_name']}"
            user_position = f"{employee['user_position']}"
            text_message += f"{n}. {first_name} {last_name},\
            \n{user_id} - ID сотрдуника,\
            \nДолжность: {user_position}\n\n"
            n += 1

        await bot.send_message(chat_id=callback_query.from_user.id,
                               text=text_message)
        await bot.delete_message(chat_id=callback_query.from_user.id,
                                 message_id=callback_query.message.message_id)
        await bot.send_message(chat_id=callback_query.from_user.id,
                               text="Главное меню!",
                               reply_markup=director_kb_main_menu)
    except Exception:
        await bot.delete_message(chat_id=callback_query.from_user.id,
                                 message_id=callback_query.message.message_id)
        await bot.send_message(chat_id=callback_query.from_user.id,
                               text="Что-то пошло не так :(")


class FSM_remove_employee(StatesGroup):
    user_id = State()


@dp.callback_query_handler(text="remove_employee")
async def remove_employee_cd(callback_query: types.CallbackQuery):
    await FSM_remove_employee.user_id.set()
    await bot.delete_message(chat_id=callback_query.from_user.id,
                             message_id=callback_query.message.message_id)
    await bot.send_message(chat_id=callback_query.from_user.id,
                           text="Введите ID пользователя для удаления.\n")


@dp.message_handler(state=FSM_remove_employee.user_id)
async def remove_employee(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        try:
            row = await check_shop_from_user(int(message.text))
            data['id'] = message.text
            id = int(data['id'])
            await delete_user(user_id=id)
            await state.finish()
            await bot.send_message(chat_id=message.from_user.id,
                                   text=f"ID пользователя: {id}\n"
                                   f"Роль пользователя {row}\n"
                                   "Удалена",
                                   reply_markup=director_kb_main_menu)
        except TypeError:
            await state.finish()
            await bot.send_message(chat_id=message.from_user.id,
                                   text=f"ID пользователя: {message.text}\n"
                                   "Ошибка. Нет такого ID пользователя\n"
                                   "\nПопробуйте ещё раз",
                                   reply_markup=director_kb_main_menu)


@dp.callback_query_handler(text="type_of_operation")
async def type_of_operation_cd(callback_query: types.CallbackQuery):
    await bot.delete_message(chat_id=callback_query.from_user.id,
                             message_id=callback_query.message.message_id)
    await bot.send_message(chat_id=callback_query.from_user.id,
                           text="Что хотите посчитать?",
                           reply_markup=director_kb_operations)


@dp.callback_query_handler(text="analysis_of_delivery")
async def analysis_of_delivery(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    shop_id = await get_shop(user_id=user_id)
    list_employees = await get_employees(shop_id=shop_id[0])
    global director_kb_view_employees
    director_kb_view_employees = types.InlineKeyboardMarkup(row_width=2)
    start_productivity_btn = types.InlineKeyboardButton(
        text="Начать подсчет продуктивности",
        callback_data="start_productivity",
    )
    for i in list_employees:
        director_kb_view_employees.add(
            types.InlineKeyboardButton(
                text=f"{i['first_name']} {i['last_name']}",
                callback_data=f"{i['user_id']}")
        )
    director_kb_view_employees.add(start_productivity_btn)
    await bot.delete_message(chat_id=callback_query.from_user.id,
                             message_id=callback_query.message.message_id)
    await bot.send_message(chat_id=callback_query.from_user.id,
                           text="Выберите нужных сотрудников для подсчета",
                           reply_markup=director_kb_view_employees)


user_selected_options = []
user_full_name = []


@dp.callback_query_handler(filters.Regexp(regexp='\d+'))
async def choose_user(callback_query: types.CallbackQuery):
    out_name_user = await get_employee_from_users(
        user_id=int(callback_query.data))
    full_name = out_name_user['first_name'] + ' ' + out_name_user['last_name']
    if callback_query.data in user_selected_options:
        user_selected_options.remove(callback_query.data)
        user_full_name.remove(full_name)
        await bot.delete_message(chat_id=callback_query.from_user.id,
                                 message_id=callback_query.message.message_id)
        await bot.send_message(chat_id=callback_query.from_user.id,
                               text=f"✅ Выбранные сотрудники:"
                               f"\n {user_full_name} ",
                               reply_markup=director_kb_view_employees)
    else:
        user_selected_options.append(callback_query.data)
        user_full_name.append(full_name)
        await bot.delete_message(chat_id=callback_query.from_user.id,
                                 message_id=callback_query.message.message_id)
        await bot.send_message(chat_id=callback_query.from_user.id,
                               text=f"✅ Выбранные сотрудники:"
                               f"\n {user_full_name}",
                               reply_markup=director_kb_view_employees)


class FSM_analyze_productivity(StatesGroup):
    number_of_units = State()


@dp.callback_query_handler(text="start_productivity")
async def start_productivity(callback_query: types.CallbackQuery):
    global start_time
    start_time = datetime.now()
    await bot.delete_message(chat_id=callback_query.from_user.id,
                             message_id=callback_query.message.message_id)
    await bot.send_message(chat_id=callback_query.from_user.id,
                           text=f"Начался подсчет продуктивности,\
                           \nВремя начала: {start_time}",
                           reply_markup=director_kb_stop_productivitty)


@dp.callback_query_handler(text="stop_productivity")
async def stop_productivity(callback_query: types.CallbackQuery):
    await FSM_analyze_productivity.number_of_units.set()
    global stop_time
    stop_time = datetime.now()
    global time_spent
    time_spent = stop_time - start_time
    await bot.delete_message(chat_id=callback_query.from_user.id,
                             message_id=callback_query.message.message_id)
    await bot.send_message(chat_id=callback_query.from_user.id,
                           text=f"Вы закончили подсчет продуктивности,\
                           \nВремя старта: {start_time}\
                           \nВремя окончания: {stop_time}\
                           \n\n Введите кол-во единиц поставки")


@dp.message_handler(state=FSM_analyze_productivity.number_of_units)
async def add_number_of_units(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        check_text = int(message.text)
        if isinstance(check_text, int):
            data['num_of_units'] = message.text
            units = int(data['num_of_units'])
            total_time = round(time_spent.seconds * len(
                user_selected_options) / 3600, 3)
            productivity = units // total_time
            for i in user_selected_options:
                await create_productivity(user_id=int(i),
                                          start_time=start_time,
                                          end_time=stop_time,
                                          num_of_units=units,
                                          productivity=productivity)
            await state.finish()
            await bot.send_message(chat_id=message.from_user.id,
                                   text=f"Расчет продуктивности окончен \
                                    \nОбщее затраченное время: {total_time} ч.\
                                    \n Продуктивность: {productivity} ед.\ч.!",
                                   reply_markup=director_kb_main_menu)
        else:
            await state.finish()
            await bot.send_message(chat_id=message.from_user.id,
                                   text=f"Это не число: {message.text}",
                                   reply_markup=director_kb_main_menu)


@dp.callback_query_handler(text="raiting_of_store")
async def check_shop_productivity(callback_query: types.CallbackQuery):
    list_shops = await check_avg_productivity_shops()
    n = 1
    text_message = ''
    try:
        for shop in list_shops:
            shop_id = shop['shop_id']
            avg_prod = shop['avg']
            text_message += f"{n}. Номер магазина: {shop_id}\
                \nСредняя продуктивность разбора {avg_prod:.1f}\n\n"
            n += 1

        await bot.send_message(chat_id=callback_query.from_user.id,
                               text=text_message)
        await bot.delete_message(chat_id=callback_query.from_user.id,
                                 message_id=callback_query.message.message_id)
        await bot.send_message(chat_id=callback_query.from_user.id,
                               text="Главное меню!",
                               reply_markup=director_kb_main_menu)
    except Exception:
        await bot.delete_message(chat_id=callback_query.from_user.id,
                                 message_id=callback_query.message.message_id)
        await bot.send_message(chat_id=callback_query.from_user.id,
                               text="Что-то пошло не так :(",
                               reply_markup=director_kb_main_menu)


@dp.callback_query_handler(text="raiting_inside_store")
async def check_employees_productivity_in_shop(
    callback_query: types.CallbackQuery
):
    shop_id = await check_shop_from_user(callback_query.from_user.id)
    list_employees = await check_avg_productivity_users_in_shop(
        shop_id=shop_id
    )
    n = 1
    text_message = ''
    try:
        for employee in list_employees:
            user_position = employee['user_position']
            first_name = employee['first_name']
            last_name = employee['last_name']
            avg_prod = employee['user_prod']
            text_message += f"{n}. {first_name} {last_name}\
                \nДолжность сотрудника: {user_position}\
                \nСредняя продуктивность разбора {avg_prod:.1f}\n\n"
            n += 1

        await bot.send_message(chat_id=callback_query.from_user.id,
                               text=text_message)
        await bot.delete_message(chat_id=callback_query.from_user.id,
                                 message_id=callback_query.message.message_id)
        await bot.send_message(chat_id=callback_query.from_user.id,
                               text="Главное меню!",
                               reply_markup=director_kb_main_menu)
    except Exception:
        await bot.delete_message(chat_id=callback_query.from_user.id,
                                 message_id=callback_query.message.message_id)
        await bot.send_message(chat_id=callback_query.from_user.id,
                               text="Что-то пошло не так :(",
                               reply_markup=director_kb_main_menu)


@dp.callback_query_handler(text="statistic_by_day")
async def check_productivity_by_days(
    callback_query: types.CallbackQuery
):
    shop_id = await check_shop_from_user(callback_query.from_user.id)
    list_by_days = await check_avg_productivity_by_day(
        shop_id=shop_id
    )
    text_message = ''
    try:
        for days in list_by_days:
            date = f"{days['start_time']}"
            avg_prod = days['avg']
            text_message += f"Дата разбора: {date}\
                \nСредняя продуктивность разбора {avg_prod:.1f}\n\n"

        await bot.send_message(chat_id=callback_query.from_user.id,
                               text=text_message)
        await bot.delete_message(chat_id=callback_query.from_user.id,
                                 message_id=callback_query.message.message_id)
        await bot.send_message(chat_id=callback_query.from_user.id,
                               text="Главное меню!",
                               reply_markup=director_kb_main_menu)
    except Exception:
        await bot.delete_message(chat_id=callback_query.from_user.id,
                                 message_id=callback_query.message.message_id)
        await bot.send_message(chat_id=callback_query.from_user.id,
                               text="Что-то пошло не так :(",
                               reply_markup=director_kb_main_menu)
