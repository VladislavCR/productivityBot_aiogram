from aiogram import types
from aiogram.dispatcher import FSMContext

from config.bot_config import bot, dp
from keyboards.admin_kb import (admin_kb_main_menu,
                                admin_kb_add_shop,
                                admin_kb_cr,
                                admin_kb_mo,
                                admin_kb_sin,
                                admin_kb_re,
                                admin_kb_xc)
from keyboards.director_kb import director_kb_main_menu
from keyboards.employee_kb import (employee_kb_registration,
                                   employee_registed_kb)
from database.users.view_users import get_employees
from database.users.check_shop_user import check_shop_from_user


@dp.callback_query_handler(text="view_list")
async def view_list(callback_query: types.CallbackQuery):
    shop_id = await check_shop_from_user(callback_query.from_user.id)
    employees = await get_employees(shop_id=shop_id)
    n = 1
    text_message = ''
    try:
        for employee in employees:
            user_id = f"{employee['user_id']}"
            first_name = f"{n}. {employee['first_name']}"
            last_name = f"{employee['last_name']}"
            user_position = f"{employee['user_position']}"
            n += 1
            text_message += f"{first_name} {last_name}, \n{user_id} - ID сотрдуника, \nДолжность: {user_position}\n\n"
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



@dp.callback_query_handler(text="remove_employee")
async def remove_employee(callback_query: types.CallbackQuery):

