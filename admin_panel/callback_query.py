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


@dp.message_handler(commands=['cancel'], state='*')
async def cancel_cmd(message: types.Message, state: FSMContext):
    curr_state = await state.get_state()
    if curr_state is None:
        return
    else:
        await state.finish()
        await bot.delete_message(chat_id=message.from_user.id,
                                 message_id=message.message_id)
        await bot.send_message(
            chat_id=message.from_user.id,
            text='Вы прервали операцию\
                \nВыбери в меню следующий шаг')


@dp.message_handler(commands=['start'])
async def start_cmd(message: types.Message):
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name
    user_id = int(message.from_user.id)
    check_user_role = await check_bd_user_role(user_id=user_id)
    await bot.delete_message(chat_id=message.from_user.id,
                             message_id=message.message_id)
    if check_user_role == 'admin':
        await bot.send_message(chat_id=message.from_user.id,
                               text=f'Привет! {first_name} {last_name}\
                                \n Твой статус: администратор бота ',
                               reply_markup=admin_kb_choices_menu)
    elif check_user_role == 'director':
        await bot.send_message(chat_id=message.from_user.id,
                               text=f'Привет! {first_name} {last_name}\
                                \n Твой статус: директор',
                               reply_markup=director_kb_main_menu)
    elif check_user_role == 'employee':
        await bot.send_message(chat_id=message.from_user.id,
                               text=f'Добро пожаловать,\
                                {first_name} {last_name}\
                                \n Твой статус: сотрудник',
                               reply_markup=employee_registed_kb)
    else:
        await bot.send_message(chat_id=message.from_user.id,
                               text='Добро пожаловать! Давай зарегистрируемся',
                               reply_markup=employee_kb_registration)


@dp.message_handler(commands=['help'])
async def cancel_cmd(message: types.Message):
    await bot.delete_message(
        chat_id=message.from_user.id,
        message_id=message.message_id)
    user_id = int(message.from_user.id)
    check_user_role = await check_bd_user_role(user_id=user_id)
    if check_user_role == 'admin':
        await bot.send_message(
            chat_id=message.from_user.id,
            text='Назначить права - дать права директора/администратора бота,\
                \n\nУбрать права сотрудника - меняет роль сотрудника на employee,\
                \n\nДобавить магазин - добавляет магазин в базу данных\
                \n\nпосмотри в базе данных ID сотрудника перед началом',
            reply_markup=admin_kb_choices_menu)
    elif check_user_role == 'director':
        await bot.send_message(
            chat_id=message.from_user.id,
            text='Посмотреть список сотрудников - выведет всех сотрудников зарегстрированных на твой магазин\
            \n\n Удалить уволенного сотрудника - удалит из базы сотдруника по ID, предварительно посмотри его в списке сотрудников\
            \n\n Общий рейтинг среди магазинов - покажет список всех магазинов ренда со средней продуктивностью \
            \n\n Рейтинг сотрудников - рейтинг сотрудников магазина за все время\
            \n\n Статистика по дням - список со средней продуктивностью за каждый день\
            \n\n Подсчет продуктивности - меню для выбора вида продуктивности и начала подсчета',
            reply_markup=director_kb_main_menu)
    elif check_user_role == 'employee':
        await bot.send_message(
            chat_id=message.from_user.id,
            text='Продуктивность по неделям - показывает твою среднюю скорость работы за каждую неделю\
            \n\n Продуктивность по дням - показывает твою среднюю продуктивность за каждый день\
            \n\n Продуктивность магазина по неделям - рейтинг сотрудников внутри твоего магазина за каждую неделю\
            \n\n 30 лучших сотрудников бренда - покажет лучших сотрудников бренда за все время',
            reply_markup=employee_registed_kb)


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


@dp.callback_query_handler(text="admin_go_back_main_menu")
async def admin_back_to_main_menu(callback_query: types.CallbackQuery):
    await bot.delete_message(chat_id=callback_query.from_user.id,
                             message_id=callback_query.message.message_id)
    await bot.send_message(chat_id=callback_query.from_user.id,
                           text="Главное меню!",
                           reply_markup=admin_kb_main_menu)


@dp.callback_query_handler(text="dir_back_to_main_menu")
async def director_back_to_main_menu(callback_query: types.CallbackQuery):
    await bot.delete_message(chat_id=callback_query.from_user.id,
                             message_id=callback_query.message.message_id)
    await bot.send_message(chat_id=callback_query.from_user.id,
                           text="Главное меню!",
                           reply_markup=director_kb_main_menu)
