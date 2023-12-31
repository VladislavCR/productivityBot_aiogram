from datetime import datetime
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import filters

from config.bot_config import bot, dp
from config.message_function import delete_and_send_message
from keyboards.director_kb import (director_kb_main_menu,
                                   director_kb_operations)
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
        await bot.send_message(
            chat_id=callback_query.from_user.id,
            text=text_message)
        await delete_and_send_message(
            callback_query.from_user.id,
            callback_query.message.message_id,
            text_message="Главное меню",
            reply_markup=director_kb_main_menu)

    except Exception:
        await delete_and_send_message(
            callback_query.from_user.id,
            callback_query.message.message_id,
            text_message="Ошибка.Нет данных для отображения"
            "\n Обратитесь к вашему РДП",
            reply_markup=director_kb_main_menu)


class FSM_remove_employee(StatesGroup):
    user_id = State()


@dp.callback_query_handler(text="remove_employee")
async def remove_employee_cd(callback_query: types.CallbackQuery):
    await FSM_remove_employee.user_id.set()
    await delete_and_send_message(
            callback_query.from_user.id,
            callback_query.message.message_id,
            text_message="Введите ID пользователя для удаления.",
            reply_markup=director_kb_main_menu)


@dp.message_handler(state=FSM_remove_employee.user_id)
async def remove_employee(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        try:
            if message.text.isdigit():
                shop_row = await check_shop_from_user(int(message.text))
                data['id'] = message.text
                id = int(data['id'])
                await delete_user(user_id=id)
                await state.finish()
                await delete_and_send_message(
                    message.from_user.id,
                    message.message_id,
                    text_message=f"ID пользователя: {id}\n"
                    f"Удален из магазина {shop_row}",
                    reply_markup=director_kb_main_menu
                )
            else:
                await delete_and_send_message(
                    message.from_user.id,
                    message.message_id,
                    text_message=f"Некорректный ввод: {message.text}"
                    f"Используй только цифры",
                    reply_markup=director_kb_main_menu
                )
        except TypeError:
            await delete_and_send_message(
                message.from_user.id,
                message.message_id,
                text_message=f"Некорректный ввод: {message.text}"
                f"Используй только цифры"
                "\n Для отмены используй меню (/cancel)",
                reply_markup=director_kb_main_menu
            )


@dp.callback_query_handler(text="type_of_operation")
async def type_of_operation_cd(callback_query: types.CallbackQuery):
    await delete_and_send_message(
            callback_query.from_user.id,
            callback_query.message.message_id,
            text_message="Что хотите посчитать?",
            reply_markup=director_kb_operations)


@dp.callback_query_handler(text="analysis_of_delivery")
async def analysis_of_delivery(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    shop_id = await get_shop(user_id=user_id)
    list_employees = await get_employees(shop_id=shop_id[0])
    global director_kb_view_employees
    director_kb_view_employees = types.InlineKeyboardMarkup(row_width=1)
    start_productivity_btn = types.InlineKeyboardButton(
        text="Начать подсчет продуктивности",
        callback_data="start_productivity",
    )
    stop_button_prod = types.InlineKeyboardButton(
        text="Остановить подсчет продуктивности",
        callback_data="stop_productivity"
    )
    for i in list_employees:
        director_kb_view_employees.add(
            types.InlineKeyboardButton(
                text=f"{i['first_name']} {i['last_name']}",
                callback_data=f"{i['user_id']}")
        )
    director_kb_view_employees.add(start_productivity_btn, stop_button_prod)
    await delete_and_send_message(
            callback_query.from_user.id,
            callback_query.message.message_id,
            text_message="Выберите нужных сотрудников для подсчета",
            reply_markup=director_kb_view_employees)


class FSM_analyze_productivity(StatesGroup):
    number_of_units = State()


@dp.callback_query_handler(
        filters.Regexp(regexp='^[0-9]+$'),
        state=None
)
async def choose_user(callback_query: types.CallbackQuery, state: FSMContext):
    out_name_user = await get_employee_from_users(
        user_id=int(callback_query.data))
    full_name = out_name_user['first_name'] + ' ' + out_name_user['last_name']
    async with state.proxy() as data:
        if callback_query.data in data.keys():
            del data[callback_query.data]
            await delete_and_send_message(
                callback_query.from_user.id,
                callback_query.message.message_id,
                text_message=f"✅ Выбранные сотрудники:"
                f"\n {list(data.values())} ",
                reply_markup=director_kb_view_employees)
        else:
            data.setdefault(callback_query.data, []).append(full_name)
            await delete_and_send_message(
                callback_query.from_user.id,
                callback_query.message.message_id,
                text_message=f"✅ Выбранные сотрудники:"
                f"\n {list(data.values())} ",
                reply_markup=director_kb_view_employees)


@dp.callback_query_handler(
        text="start_productivity",
        state=None
)
async def start_productivity(
    callback_query: types.CallbackQuery,
    state: FSMContext
):
    async with state.proxy() as data:
        start_time = datetime.now().strftime("%X-%W")
        print(start_time)
        for key in data:
            data.setdefault(key, []).extend([start_time])
        data['start_time'] = start_time
        await delete_and_send_message(
            callback_query.from_user.id,
            callback_query.message.message_id,
            text_message=f"Начался подсчет продуктивности,\
            \nВремя начала: {start_time}",
            reply_markup=director_kb_view_employees)


@dp.callback_query_handler(text="stop_productivity")
async def stop_productivity(callback_query: types.CallbackQuery):
    await FSM_analyze_productivity.number_of_units.set()
    global stop_time
    stop_time = datetime.now()
    global time_spent
    time_spent = stop_time - start_time
    await delete_and_send_message(
            callback_query.from_user.id,
            callback_query.message.message_id,
            text_message=f"Вы закончили подсчет продуктивности,\
            \nВремя старта: {start_time}\
            \nВремя окончания: {stop_time}\
            \n\n Введите кол-во единиц поставки",
            reply_markup=None)


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
        await delete_and_send_message(
            callback_query.from_user.id,
            callback_query.message.message_id,
            text_message="Главное меню!",
            reply_markup=director_kb_main_menu)
    except Exception:
        await delete_and_send_message(
            callback_query.from_user.id,
            callback_query.message.message_id,
            text_message="Нет данных для отображения, "
            "\nобратись к своему РДП",
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
        await delete_and_send_message(
            callback_query.from_user.id,
            callback_query.message.message_id,
            text_message="Главное меню!",
            reply_markup=director_kb_main_menu)
    except Exception:
        await delete_and_send_message(
            callback_query.from_user.id,
            callback_query.message.message_id,
            text_message="Нет данных для отображения, "
            "\nобратись к своему РДП",
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
        await delete_and_send_message(
            callback_query.from_user.id,
            callback_query.message.message_id,
            text_message="Главное меню!",
            reply_markup=director_kb_main_menu)
    except Exception:
        await delete_and_send_message(
            callback_query.from_user.id,
            callback_query.message.message_id,
            text_message="Нет данных для отображения, "
            "\nобратись к своему РДП",
            reply_markup=director_kb_main_menu)
