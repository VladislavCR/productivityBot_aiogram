from aiogram import types
from config.bot_config import dp, bot
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from keyboards.admin_kb import admin_kb_add_rights, admin_kb_main_menu
from database.user_role.check_role import check_bd_user_role, check_user
from database.user_role.create_role import create_admin, create_director
from database.users.delete_user import delete_user


@dp.callback_query_handler(text="add_rights", state=None)
async def add_rights(callback_query: types.CallbackQuery):
    await bot.delete_message(chat_id=callback_query.from_user.id,
                             message_id=callback_query.message.message_id)
    await bot.send_message(chat_id=callback_query.from_user.id,
                           text='Выбери роль сотрудника!',
                           reply_markup=admin_kb_add_rights)


class FSM_create_user_role_admin(StatesGroup):
    user_id = State()


@dp.callback_query_handler(text="make_user_admin", state=None)
async def load_user_role_admin(callback_query: types.CallbackQuery):
    await FSM_create_user_role_admin.user_id.set()
    await bot.delete_message(chat_id=callback_query.from_user.id,
                             message_id=callback_query.message.message_id)
    await bot.send_message(chat_id=callback_query.from_user.id,
                           text="Роль успешно выбрана.\n"
                           "\nВведите user_id пользователя,"
                           "которого хотите назначить администратором:")


@dp.message_handler(state=FSM_create_user_role_admin.user_id)
async def load_user_id_admin(message: types.Message, state: FSMContext):
    print(message.text)
    try:
        float(message.text)
        test_check_user = await check_user(user_id=int(message.text))
        if test_check_user:
            test = await check_bd_user_role(user_id=int(message.text))
            if test == 'admin':
                await state.finish()
                await bot.send_message(
                    chat_id=message.from_user.id,
                    text=f"\nОшибка ID пользователя уже используется"
                    f"\nЭто Админ\n"
                    f"\nID пользователя:  {message.text}\n"
                    f"\nПопробуйте снова",
                    reply_markup=admin_kb_main_menu)
            elif test == 'director':
                await state.finish()
                await bot.send_message(
                    chat_id=message.from_user.id,
                    text=f"\nОшибка ID пользователя уже используется"
                    f"\nЭто Директор\n"
                    f"\nID пользователя:  {message.text}\n"
                    f"\nПопробуйте снова",
                    reply_markup=admin_kb_main_menu)
            else:
                async with state.proxy() as data:
                    data['user_id'] = message.text
                    str_data = str(data['user_id'])
                    int_data = int(str_data)
                    await state.finish()
                    await create_admin(user_id=int_data)
                    await bot.send_message(
                        chat_id=message.from_user.id,
                        text=f"\nАдминистратор\n"
                        f"ID пользователя:  {int_data}\n",
                        reply_markup=admin_kb_main_menu)
        else:
            await state.finish()
            await bot.send_message(
                chat_id=message.from_user.id,
                text=f"Сотрдуник с ID "
                f"{message.text} не существует\n"
                f"Создайте сотрудника в базе данных",
                reply_markup=admin_kb_main_menu)  # Поменять клавиатуру на директорскую
    except ValueError:
        await state.finish()
        await bot.send_message(chat_id=message.from_user.id,
                               text=f"\nОшибка ID пользователя (Это не число)"
                               f"\nID пользователя:  {message.text}\n"
                               f"\nПопробуйте снова",
                               reply_markup=admin_kb_main_menu)


class FSM_create_user_role_director(StatesGroup):
    user_id = State()


@dp.callback_query_handler(text="make_user_director", state=None)
async def load_user_role_director(callback_query: types.CallbackQuery):
    await FSM_create_user_role_director.user_id.set()
    await bot.delete_message(chat_id=callback_query.from_user.id,
                             message_id=callback_query.message.message_id)
    await bot.send_message(chat_id=callback_query.from_user.id,
                           text="Роль успешно выбрана.\n"
                           "\nВведите user_id пользователя,"
                           "которого хотите назначить директором:")


@dp.message_handler(state=FSM_create_user_role_director.user_id)
async def load_user_id_director(message: types.Message, state: FSMContext):
    try:
        float(message.text)
        test_check_user = await check_user(user_id=int(message.text))
        if test_check_user:
            test = await check_bd_user_role(user_id=int(message.text))
            if test == 'admin':
                await state.finish()
                await bot.send_message(
                    chat_id=message.from_user.id,
                    text=f"\nОшибка ID пользователя уже используется"
                    f"\nЭто Админ\n"
                    f"\nID пользователя:  {message.text}\n"
                    f"\nПопробуйте снова",
                    reply_markup=admin_kb_main_menu)
            elif test == 'director':
                await state.finish()
                await bot.send_message(
                    chat_id=message.from_user.id,
                    text=f"\nОшибка ID пользователя уже используется"
                    f"\nЭто Директор\n"
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
                        await bot.send_message(
                            chat_id=message.from_user.id,
                            text=f"\nОшибка, ID пользователя "
                            "не может быть отрицательным\n"
                            f"ID пользователя:  {str_data}\n"
                            f"\nПопробуйте снова",
                            reply_markup=admin_kb_main_menu)
                    else:
                        async with state.proxy() as data:
                            data['user_id'] = message.text
                            str_data = str(data['user_id'])
                            int_data = int(str_data)
                            await state.finish()
                            await create_director(user_id=int_data)
                            await bot.send_message(
                                chat_id=message.from_user.id,
                                text=f"\nАдминистратор\n"
                                f"ID пользователя:  {int_data}\n",
                                reply_markup=admin_kb_main_menu)
        else:
            await state.finish()
            await bot.send_message(
                chat_id=message.from_user.id,
                text=f"Сотрдуник с ID {message.text}"
                " не существует\n"
                f"Создайте сотрудника в базе данных",
                reply_markup=admin_kb_main_menu)  # Поменять клавиатуру на директорскую
    except ValueError:
        await state.finish()
        await bot.send_message(chat_id=message.from_user.id,
                               text=f"Ошибка ID пользователя (Это не число)"
                               f"\nID пользователя:  {message.text}\n"
                               f"\nПопробуйте снова",
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
