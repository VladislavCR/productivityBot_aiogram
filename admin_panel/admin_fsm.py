from aiogram import types
from config.bot_config import dp, bot
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from keyboards.admin_kb import *
from database.user_role.check_user_role import check_bd_user_role
from database.user_role.create_role import create_admin, create_director
from database.users.delete_users import delete_user


@dp.callback_query_handler(text="add_rights", state=None)
async def add_rights(callback_query: types.CallbackQuery):
    await bot.delete_message(chat_id=callback_query.from_user.id,
                             message_id=callback_query.message.message_id)
    await bot.send_message(chat_id=callback_query.from_user.id,
                           text='Выбери роль сотрудника!',
                           reply_markup=admin_kb_add_rights)


class FSM_create_user_role_admin(StatesGroup):
    user_id = State()
    user_first_name = State()
    user_last_name = State()
    user_position = State()


@dp.callback_query_handler(text="make_user_admin", state=None)
async def load_user_role_admin(callback_query: types.CallbackQuery):
    await FSM_create_user_role_admin.user_id.set()
    await bot.delete_message(chat_id=callback_query.from_user.id,
                             message_id=callback_query.message.message_id)
    await bot.send_message(chat_id=callback_query.from_user.id,
                           text=f"Роль успешно выбрана.\n"
                           f"\nВведите user_id пользователя,"
                           f"которого хотите назначить администратором:")


@dp.message_handler(state=FSM_create_user_role_admin.user_id)
async def load_user_id(message: types.Message, state: FSMContext):
    try:
        float(message.text)
        test = await check_bd_user_role(id=int(message.text))
        if test == 'admin':
            await state.finish()
            await bot.send_message(chat_id=message.from_user.id,
                               text=f"\nОшибка ID пользователя уже используется"
                               f"\nЭто Админ\n"
                               f"\nID пользователя:  {message.text}\n"
                               f"\nПопробуйте снова",
                               reply_markup=admin_kb_main_menu)
        elif test == 'director':
            await state.finish()
            await bot.send_message(chat_id=message.from_user.id,
                               text=f"\nОшибка ID пользователя уже используется"
                               f"\nЭто Директор\n"
                               f"\nID пользователя:  {message.text}\n"
                               f"\nПопробуйте снова",
                               reply_markup=admin_kb_main_menu)
        elif test == 'staff':
            await state.finish()
            await bot.send_message(chat_id=message.from_user.id,
                               text=f"\nОшибка ID пользователя уже используется"
                               f"\nЭто Продавец\n"
                               f"\nID пользователя:  {message.text}\n"
                               f"\nПопробуйте снова",
                               reply_markup=admin_kb_main_menu)
        else:
            async with state.proxy() as data:
                data['id'] = message.text
                # Записываем в дату в виде строки
                str_data = str(data['id'])
                # Записываем в дату в виде числа
                int_data = int(str_data)
                if int_data < 0:
                    await state.finish()
                    await bot.send_message(chat_id=message.from_user.id,
                                           text=f"\nОшибка ID пользователя не может быть отрицательным\n"
                                           f"ID пользователя:  {str_data}\n"
                                           f"\nПопробуйте снова",
                                           reply_markup=admin_kb_main_menu)
                else:
                    await FSM_create_user_role_admin.next()
                    await bot.send_message(chat_id=message.from_user.id,
                                           text=f"\nАдминистратор\n"
                                           f"ID пользователя:  {int_data}\n"
                                           f"\nВведите имя: ")
    except ValueError:
        await state.finish()
        await bot.send_message(chat_id=message.from_user.id,
                                       text=f"\nОшибка ID пользователя (Это не число)\n"
                                       f"ID пользователя:  {message.text}\n"
                                       f"\nПопробуйте снова",
                                       reply_markup=admin_kb_main_menu)

@dp.message_handler(state=FSM_create_user_role_admin.user_first_name)
async def load_user_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        res = isinstance(message.text, str)
        if res is True:
            # Записываем в дату указанный user_name в сообщении
            data['user_first_name'] = message.text
            await FSM_create_user_role_admin.next()
            await bot.send_message(chat_id=message.from_user.id,
                                   text=f"Имя: {data['user_first_name']}\n"
                                   f"\nВведите фамилию: ")
        else:
            await state.finish()
            await bot.send_message(chat_id=message.from_user.id,
                                       text=f"\nОшибка вы прислали не строку\n"
                                       f"ID пользователя:  {data['id']}\n"
                                       f"Имя пользователя:  {message.text}\n"
                                       f"\nПопробуйте ещё раз",
                                       reply_markup=admin_kb_main_menu)


@dp.message_handler(state=FSM_create_user_role_admin.user_last_name)
async def load_user_last_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        res = isinstance(message.text, str)
        if res is True:
            data['user_last_name'] = message.text
            await FSM_create_user_role_admin.next()
            await bot.send_message(chat_id=message.from_user.id,
                                   text=f"Фамилия: {data['user_last_name']}\n"
                                   f"\nВведите должность: ")
        else:
            await state.finish()
            await bot.send_message(chat_id=message.from_user.id,
                                       text=f"\nОшибка вы прислали не строку\n"
                                       f"ID пользователя:  {data['id']}\n"
                                       f"Фамилия пользователя:  {message.text}\n"
                                       f"\nПопробуйте ещё раз",
                                       reply_markup=admin_kb_main_menu)


@dp.message_handler(state=FSM_create_user_role_admin.user_position)
async def load_user_position(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        res = isinstance(message.text, str)
        if res is True:
            data['user_position'] = message.text
            int_data_user_id = int(data['id'])
            await create_admin(id=int_data_user_id,
                               user_first_name=data['user_first_name'],
                               user_last_name=data['user_last_name'],
                               user_position=data['user_position'])
            await bot.send_message(chat_id=message.from_user.id,
                                       text=f"\nАдминистратор\n"
                                       f"ID пользователя:  {int_data_user_id}\n"
                                       f"ФИО пользователя:  {data['user_first_name']} {data['user_last_name']}\n"
                                       f"Должность пользователя:  {data['user_position']}\n"
                                       f"\nРоль админа успешно присвоена.",
                                       reply_markup=admin_kb_main_menu)
            await state.finish()
        else:
            await state.finish()
            await bot.send_message(chat_id=message.from_user.id,
                                       text=f"\nОшибка вы прислали не строку\n"
                                       f"ID пользователя:  {data['id']}\n"
                                       f"Должность пользователя:  {message.text}\n"
                                       f"\nПопробуйте ещё раз",
                                       reply_markup=admin_kb_main_menu)


class FSM_create_user_role_director(StatesGroup):
    user_id = State()
    user_first_name = State()
    user_last_name = State()
    user_position = State()


@dp.callback_query_handler(text="make_user_director", state=None)
async def load_user_role_director(callback_query: types.CallbackQuery):
    await FSM_create_user_role_director.user_id.set()
    await bot.delete_message(chat_id=callback_query.from_user.id,
                             message_id=callback_query.message.message_id)
    await bot.send_message(chat_id=callback_query.from_user.id,
                           text=f"Роль успешно выбрана.\n"
                           f"\nВведите user_id пользователя,"
                           f"которого хотите назначить директором:")


@dp.message_handler(state=FSM_create_user_role_director.user_id)
async def load_user_id(message: types.Message, state: FSMContext):
    try:
        float(message.text)
        test = await check_bd_user_role(id=int(message.text))
        if test == 'admin':
            await state.finish()
            await bot.send_message(chat_id=message.from_user.id,
                               text=f"\nОшибка ID пользователя уже используется"
                               f"\nЭто Админ\n"
                               f"\nID пользователя:  {message.text}\n"
                               f"\nПопробуйте снова",
                               reply_markup=admin_kb_main_menu)
        elif test == 'director':
            await state.finish()
            await bot.send_message(chat_id=message.from_user.id,
                               text=f"\nОшибка ID пользователя уже используется"
                               f"\nЭто Директор\n"
                               f"\nID пользователя:  {message.text}\n"
                               f"\nПопробуйте снова",
                               reply_markup=admin_kb_main_menu)
        elif test == 'staff':
            await state.finish()
            await bot.send_message(chat_id=message.from_user.id,
                               text=f"\nОшибка ID пользователя уже используется"
                               f"\nЭто Продавец\n"
                               f"\nID пользователя:  {message.text}\n"
                               f"\nПопробуйте снова",
                               reply_markup=admin_kb_main_menu)
        else:
            async with state.proxy() as data:
                data['id'] = message.text
                str_data = str(data['id'])
                int_data = int(str_data)
                if int_data < 0:
                    await state.finish()
                    await bot.send_message(chat_id=message.from_user.id,
                                           text=f"\nОшибка ID пользователя не может быть отрицательным\n"
                                           f"ID пользователя:  {str_data}\n"
                                           f"\nПопробуйте снова",
                                           reply_markup=admin_kb_main_menu)
                else:
                    await FSM_create_user_role_director.next()
                    await bot.send_message(chat_id=message.from_user.id,
                                           text=f"\nДиректор\n"
                                           f"ID пользователя:  {int_data}\n"
                                           f"\nВведите имя: ")
    except ValueError:
        await state.finish()
        await bot.send_message(chat_id=message.from_user.id,
                                       text=f"\nОшибка ID пользователя (Это не число)\n"
                                       f"ID пользователя:  {message.text}\n"
                                       f"\nПопробуйте снова",
                                       reply_markup=admin_kb_main_menu)

@dp.message_handler(state=FSM_create_user_role_director.user_first_name)
async def load_user_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        res = isinstance(message.text, str)
        if res is True:
            # Записываем в дату указанный user_name в сообщении
            data['user_first_name'] = message.text
            await FSM_create_user_role_director.next()
            await bot.send_message(chat_id=message.from_user.id,
                                   text=f"Имя: {data['user_first_name']}\n"
                                   f"\nВведите фамилию: ")
        else:
            await state.finish()
            await bot.send_message(chat_id=message.from_user.id,
                                       text=f"\nОшибка вы прислали не строку\n"
                                       f"ID пользователя:  {data['id']}\n"
                                       f"Имя пользователя:  {message.text}\n"
                                       f"\nПопробуйте ещё раз",
                                       reply_markup=admin_kb_main_menu)


@dp.message_handler(state=FSM_create_user_role_director.user_last_name)
async def load_user_last_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        res = isinstance(message.text, str)
        if res is True:
            data['user_last_name'] = message.text
            await FSM_create_user_role_director.next()
            await bot.send_message(chat_id=message.from_user.id,
                                   text=f"Фамилия: {data['user_last_name']}\n"
                                   f"\nВведите должность: ")
        else:
            await state.finish()
            await bot.send_message(chat_id=message.from_user.id,
                                       text=f"\nОшибка вы прислали не строку\n"
                                       f"ID пользователя:  {data['id']}\n"
                                       f"Фамилия пользователя:  {message.text}\n"
                                       f"\nПопробуйте ещё раз",
                                       reply_markup=admin_kb_main_menu)


@dp.message_handler(state=FSM_create_user_role_director.user_position)
async def load_user_position(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        res = isinstance(message.text, str)
        if res is True:
            data['user_position'] = message.text
            int_data_user_id = int(data['id'])
            await create_director(id=int_data_user_id,
                               user_first_name=data['user_first_name'],
                               user_last_name=data['user_last_name'],
                               user_position=data['user_position'])
            await bot.send_message(chat_id=message.from_user.id,
                                       text=f"\nДиректор\n"
                                       f"ID пользователя:  {int_data_user_id}\n"
                                       f"ФИО пользователя:  {data['user_first_name']} {data['user_last_name']}\n"
                                       f"Должность пользователя:  {data['user_position']}\n"
                                       f"\nРоль директора успешно присвоена.",
                                       reply_markup=admin_kb_main_menu)
            await state.finish()
        else:
            await state.finish()
            await bot.send_message(chat_id=message.from_user.id,
                                       text=f"\nОшибка вы прислали не строку\n"
                                       f"ID пользователя:  {data['id']}\n"
                                       f"Должность пользователя:  {message.text}\n"
                                       f"\nПопробуйте ещё раз",
                                       reply_markup=admin_kb_main_menu)


class FSM_delete_user_role(StatesGroup):
    user_id = State()

@dp.callback_query_handler(text="remove_rights")
async def remove_rights(callback_query: types.CallbackQuery):
    await FSM_delete_user_role.user_id.set()
    await bot.delete_message(chat_id=callback_query.from_user.id,
                             message_id=callback_query.message.message_id)
    await bot.send_message(chat_id=callback_query.from_user.id,
                           text="Введите ID записи для удаления.\n")


@dp.message_handler(state=FSM_delete_user_role.user_id)
async def delete_user_role(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        try:
            row = await check_bd_user_role(int(message.text))
            data['id'] = str(message.text)
            id = int(data['id'])
            await delete_user(user_id=id)
            await state.finish()
            await bot.send_message(chat_id=message.from_user.id,
                                   text=f"ID пользователя: {id}\n"
                                   f"Роль пользователя {row}\n"
                                   "Удалена",
                                   reply_markup=admin_kb_main_menu)
        except TypeError:
            await state.finish()
            await bot.send_message(chat_id=message.from_user.id,
                                   text=f"ID пользователя: {message.text}\n"
                                   "Ошибка. Нет такого ID пользователя\n"
                                   "\nПопробуйте ещё раз",
                                   reply_markup=admin_kb_main_menu)