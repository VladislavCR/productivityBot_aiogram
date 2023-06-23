from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from config.bot_config import bot, dp
from keyboards.director_kb import (director_kb_main_menu,
                                   director_kb_operations)
from database.users.view_users import get_employees, get_shop
from database.users.check_shop_user import check_shop_from_user
from database.users.delete_user import delete_user


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
            text_message += f"{n}. {first_name} {last_name},\n \
            {user_id} - ID сотрдуника, \nДолжность: {user_position}\n\n"
            n += 1

        await bot.send_message(chat_id=callback_query.from_user.id,
                               text=text_message)
        await bot.delete_message(chat_id=callback_query.from_user.id,
                                 message_id=callback_query.message.message_id)
        await bot.send_message(chat_id=callback_query.from_user.id,
                               text="Главное меню!",
                               reply_markup=director_kb_main_menu)
    except Exception:
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
    director_kb_view_employees = types.InlineKeyboardMarkup(row_width=1)
    for i in list_employees:
        director_kb_view_employees.add(
            types.InlineKeyboardButton(
                text=f"{i['first_name']} {i['last_name']}",
                callback_data=f"{i['user_id']}")
        )
    await bot.delete_message(chat_id=callback_query.from_user.id,
                             message_id=callback_query.message.message_id)
    await bot.send_message(chat_id=callback_query.from_user.id,
                           text="Выберите нужных сотрудников для подсчета",
                           reply_markup=director_kb_view_employees)
