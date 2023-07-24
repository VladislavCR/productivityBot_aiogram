from aiogram import types
from config.bot_config import dp, bot
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from config.message_function import delete_and_send_message
from keyboards.admin_kb import admin_kb_add_rights, admin_kb_main_menu
from keyboards.director_kb import director_kb_main_menu
from database.user_role.check_role import check_bd_user_role, check_user
from database.user_role.create_role import create_admin, create_director
from database.users.delete_user import delete_user
from database.shops.check_shop import check_shop
from admin_panel.callback_query import *


@dp.callback_query_handler(text="admin_menu")
async def choice_admin_menu(callback_query: types.CallbackQuery):
    await delete_and_send_message(
            callback_query.from_user.id,
            callback_query.message.message_id,
            text_message="Ты выбрал меню супер-пользователя",
            reply_markup=admin_kb_main_menu)


@dp.callback_query_handler(text="director_menu")
async def choice_director_menu(callback_query: types.CallbackQuery):
    await delete_and_send_message(
            callback_query.from_user.id,
            callback_query.message.message_id,
            text_message="Ты выбрал меню директора"
            "\n Для возврата выбери Главное меню (/start)",
            reply_markup=director_kb_main_menu)


@dp.callback_query_handler(text="add_rights")
async def add_rights(callback_query: types.CallbackQuery):
    await delete_and_send_message(
            callback_query.from_user.id,
            callback_query.message.message_id,
            text_message="Выбери роль сотрудника",
            reply_markup=admin_kb_add_rights)


class FSM_create_user_role_admin(StatesGroup):
    user_id = State()


@dp.callback_query_handler(text="make_user_admin")
async def load_user_role_admin(callback_query: types.CallbackQuery):
    await FSM_create_user_role_admin.user_id.set()
    await delete_and_send_message(
            callback_query.from_user.id,
            callback_query.message.message_id,
            text_message="Роль успешно выбрана.\n"
                         "\nВведите user_id пользователя,"
                         "которого хотите назначить администратором "
                         "или отмените операцию в меню (/cancel)",
            reply_markup=None)


@dp.message_handler(state=FSM_create_user_role_admin.user_id)
async def load_user_id_admin(message: types.Message, state: FSMContext):
    try:
        test_check_user = await check_user(user_id=int(message.text))
        if test_check_user:
            test = await check_bd_user_role(user_id=int(message.text))
            if test == 'admin':
                await delete_and_send_message(
                    message.from_user.id,
                    message.message_id,
                    text_message=f"\nОшибка ID пользователя уже используется"
                    f"\nЭто Админ\n"
                    f"\nID пользователя:  {message.text}\n"
                    f"\nПопробуйте снова",
                    reply_markup=None
                )
            elif test == 'director':
                await delete_and_send_message(
                    message.from_user.id,
                    message.message_id,
                    text_message=f"\nОшибка ID пользователя уже используется"
                    f"\nЭто Директор\n"
                    f"\nID пользователя:  {message.text}\n"
                    f"\nПопробуйте снова",
                    reply_markup=None
                )
            else:
                async with state.proxy() as data:
                    data['user_id'] = message.text
                    int_data = int(message.text)
                    await state.finish()
                    await create_admin(user_id=int_data)
                    await delete_and_send_message(
                        message.from_user.id,
                        message.message_id,
                        text_message=f"\nАдминистратор\n"
                        f"ID пользователя:  {int_data}\n",
                        reply_markup=admin_kb_main_menu
                    )
        else:
            await delete_and_send_message(
                message.from_user.id,
                message.message_id,
                text_message="Сотрдуник с ID "
                f"{message.text} не существует\n"
                "Проверьте корректность введенных данных",
                reply_markup=admin_kb_main_menu
            )
    except ValueError:
        await delete_and_send_message(
                message.from_user.id,
                message.message_id,
                text_message=f"\nОшибка ID пользователя (Это не число)"
                f"\nID пользователя:  {message.text}\n"
                f"\nПопробуйте снова или отмените операцию в меню",
                reply_markup=admin_kb_main_menu
        )


class FSM_create_user_role_director(StatesGroup):
    user_id = State()


@dp.callback_query_handler(text="make_user_director", state=None)
async def load_user_role_director(callback_query: types.CallbackQuery):
    await FSM_create_user_role_director.user_id.set()
    await delete_and_send_message(
            callback_query.from_user.id,
            callback_query.message.message_id,
            text_message="Роль успешно выбрана.\n"
                         "\nВведите user_id пользователя,"
                         "которого хотите назначить директором "
                         "или отмените оперцию в меню (/cancel)",
            reply_markup=None)


@dp.message_handler(state=FSM_create_user_role_director.user_id)
async def load_user_id_director(message: types.Message, state: FSMContext):
    try:
        test_check_user = await check_user(user_id=int(message.text))
        if test_check_user:
            test = await check_bd_user_role(user_id=int(message.text))
            if test == 'admin':
                await delete_and_send_message(
                    message.from_user.id,
                    message.message_id,
                    text_message=f"\nОшибка ID пользователя уже используется"
                    f"\nЭто Админ\n"
                    f"\nID пользователя:  {message.text}\n"
                    f"\nПопробуйте снова",
                    reply_markup=None
                )
            elif test == 'director':
                await delete_and_send_message(
                    message.from_user.id,
                    message.message_id,
                    text_message=f"\nОшибка ID пользователя уже используется"
                    f"\nЭто Директор\n"
                    f"\nID пользователя:  {message.text}\n"
                    f"\nПопробуйте снова",
                    reply_markup=None
                )
            else:
                async with state.proxy() as data:
                    data['id'] = message.text
                    int_data = int(message.text)
                    await state.finish()
                    await create_director(user_id=int_data)
                    await delete_and_send_message(
                        message.from_user.id,
                        message.message_id,
                        text_message=f"\nДиректор\n"
                        f"ID пользователя:  {int_data}\n",
                        reply_markup=admin_kb_main_menu
                    )
        else:
            await delete_and_send_message(
                message.from_user.id,
                message.message_id,
                text_message="Сотрдуник с ID "
                f"{message.text} не существует\n"
                "Проверьте корректность введенных данных "
                "или отмените операцию в меню (/cancel)",
                reply_markup=admin_kb_main_menu
            )
    except ValueError:
        await delete_and_send_message(
                message.from_user.id,
                message.message_id,
                text_message=f"\nОшибка ID пользователя (Это не число)"
                f"\nID пользователя:  {message.text}\n"
                f"\nПопробуйте снова или отмените операцию в меню",
                reply_markup=admin_kb_main_menu
        )


class FSM_delete_user_role(StatesGroup):
    user_id = State()


@dp.callback_query_handler(text="remove_rights")
async def remove_rights(callback_query: types.CallbackQuery):
    await FSM_delete_user_role.user_id.set()
    await delete_and_send_message(
            callback_query.from_user.id,
            callback_query.message.message_id,
            text_message="Введите ID записи для удаления.\n",
            reply_markup=None)


@dp.message_handler(state=FSM_delete_user_role.user_id)
async def delete_user_role(message: types.Message, state: FSMContext):
    try:
        if message.text.isdigit():
            row = await check_bd_user_role(int(message.text))
            if row is []:
                await delete_and_send_message(
                    message.from_user.id,
                    message.message_id,
                    text_message=f"ID пользователя: {message.text}"
                    "\nОшибка. Такого ID пользователя не существует\n"
                    "Попробуйте ещё раз или "
                    "отмените операцию в меню (/cancel)",
                    reply_markup=None
                )
            else:
                await delete_user(user_id=int(message.text))
                await state.finish()
                await delete_and_send_message(
                    message.from_user.id,
                    message.message_id,
                    text_message=f"ID пользователя: {message.text}\n"
                    f"Роль пользователя {row}\n"
                    "Удалена",
                    reply_markup=admin_kb_main_menu
                )
        else:
            await delete_and_send_message(
                    message.from_user.id,
                    message.message_id,
                    text_message="Некорректный воод, используй только цифры"
                    f"\nТвой ввод: {message.text}"
                    "\nИспользуй только цифры",
                    reply_markup=admin_kb_main_menu
                )
    except TypeError:
        await state.finish()
        await delete_and_send_message(
                    message.from_user.id,
                    message.message_id,
                    text_message="Некорректный воод, используй только цифры"
                    f"\nТвой ввод: {message.text}"
                    "\nИспользуй только цифры",
                    reply_markup=admin_kb_main_menu
        )


class FSM_create_shop(StatesGroup):
    shop_id = State()
    city = State()


@dp.callback_query_handler(text="add_shop_cr", state=None)
async def add_shop_cr(callback_query: types.CallbackQuery):
    await FSM_create_shop.shop_id.set()
    await delete_and_send_message(
            callback_query.from_user.id,
            callback_query.message.message_id,
            text_message="Бренд CR, "
            "\nВведите номер магазина"
            "\n или отмени операцию в меню (/cancel)",
            reply_markup=admin_kb_main_menu)


# @dp.message_handler(state=FSM_create_shop.shop_id)
# async def load_shop_id_admin(message: types.Message, state: FSMContext):
#     try:
#         test_check_shop_id = await check_shop(shop_number=int(message.text))
#         if test_check_shop_id:
#             await state.finish()
#             await bot.send_message(
#                 chat_id=message.from_user.id,
#                 text=f"\nТакой номер магазина уже существует"
#                 f"\nПроверьте корректность ввода данных\n"
#                 f"\nНомер магазина:  {message.text}\n"
#                 f"\nПопробуйте снова",
#                 reply_markup=admin_kb_cr)
#         else:
#             async with state.proxy() as data:
#                 data['shop_id'] = message.text
