from aiogram import types
from config.bot_config import dp, bot
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from keyboards.employee_kb import (employee_kb_registration,
                                   employee_kb_return,
                                   employee_registed_kb)
from keyboards.reply_kb import choice_position_kb
from database.users.check_brand_user import check_brand_from_user
from database.users.check_shop_user import check_shop_from_user
from database.users.create_user import create_user_bd
from database.shops.check_shop import check_shop
from database.user_role.create_role import create_user
from database.productivity.check_prod_by_day import (
    check_personal_prod_by_day)
from database.productivity.check_prod_by_week import (
    check_personal_prod_by_week,
    check_top30_in_brand)
from database.productivity.check_avg_prod_shop import (
    check_avg_productivity_employees_in_shop)


class FSM_create_new_user(StatesGroup):
    first_name = State()
    last_name = State()
    user_position = State()
    shop_id = State()


@dp.callback_query_handler(text="start_reg", state=None)
async def start_registration(callback_query: types.CallbackQuery):
    await FSM_create_new_user.first_name.set()
    await bot.edit_message_text(chat_id=callback_query.from_user.id,
                                message_id=callback_query.message.message_id,
                                text="Начало регистрации!\n"
                                "Введи свое имя:",
                                reply_markup=employee_kb_return)


@dp.message_handler(state=FSM_create_new_user.first_name)
async def create_first_name(message: types.Message, state: FSMContext):
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
async def create_last_name(message: types.Message, state: FSMContext):
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
                check_bd = await check_shop(shop_id=int(message.text))
                if check_bd:
                    async with state.proxy() as data:
                        data['shop_id'] = int(message.text)
                        await state.finish()
                        await create_user_bd(
                            user_id=message.from_user.id,
                            first_name=data['first_name'],
                            last_name=data['last_name'],
                            user_position=data['user_position'],
                            shop_id=data['shop_id'])
                        await create_user(user_id=message.from_user.id)
                        await bot.send_message(
                            chat_id=message.from_user.id,
                            text=f"\nВы зарегистрированы\n"
                            f"ID пользователя:  {message.from_user.id}\n"
                            f"ФИО пользователя:  {data['first_name']}"
                            f"{data['last_name']}\n"
                            f"Должность пользователя: "
                            f"{data['user_position']}\n"
                            f"Ваш магазин: {data['shop_id']}",
                            reply_markup=employee_registed_kb)
                else:
                    await state.finish()
                    await bot.send_message(
                        chat_id=message.from_user.id,
                        text=f"\nОшибка, такого номера магазина нет в базе\n"
                        f"Номер магазина:  {message.text}\n"
                        f"\nПопробуйте ещё раз",
                        reply_markup=employee_kb_registration)
            except ValueError:
                await state.finish()
                await bot.send_message(
                    chat_id=message.from_user.id,
                    text=f"\nОшибка ID пользователя (Это не число)\n"
                    f"ID пользователя:  {message.text}\n"
                    f"\nПопробуйте снова",
                    reply_markup=employee_kb_registration)
        else:
            await state.finish()
            await bot.send_message(chat_id=message.from_user.id,
                                   text=f"\nОшибка такого номера магазине нет\
                                   \nНомер магазина:  {message.text}\
                                   \nПопробуйте ещё раз",
                                   reply_markup=employee_kb_registration,
                                   )


@dp.callback_query_handler(text="show_personal_stat_week")
async def show_personal_stat_month(
    callback_query: types.CallbackQuery
):
    user_id = callback_query.from_user.id
    list_by_weeks = await check_personal_prod_by_week(
        user_id=user_id)
    text_message = ''
    try:
        for week in list_by_weeks:
            first_name = week['first_name']
            last_name = week['last_name']
            user_prod = week['avg']
            week = week['week_number']
            text_message += f"{first_name} {last_name}:\
                \nМесяца разбора: {week:.0f}\
                \nСредняя продуктивность разбора {user_prod:.1f}\n\n"

        await bot.send_message(chat_id=callback_query.from_user.id,
                               text=text_message)
        await bot.delete_message(chat_id=callback_query.from_user.id,
                                 message_id=callback_query.message.message_id)
        await bot.send_message(chat_id=callback_query.from_user.id,
                               text="Ваша продуктивность по неделям\
                               в сообщении",
                               reply_markup=employee_registed_kb)
    except Exception:
        await bot.delete_message(chat_id=callback_query.from_user.id,
                                 message_id=callback_query.message.message_id)
        await bot.send_message(chat_id=callback_query.from_user.id,
                               text="Что-то пошло не так :(",
                               reply_markup=employee_registed_kb)


@dp.callback_query_handler(text="show_personal_stat_day")
async def show_personal_stat_day(
    callback_query: types.CallbackQuery
):
    user_id = callback_query.from_user.id
    list_by_days = await check_personal_prod_by_day(
        user_id=user_id)
    text_message = ''
    try:
        for day in list_by_days:
            user_prod = day['user_prod']
            first_name = day['first_name']
            last_name = day['last_name']
            day = day['day_number']
            text_message += f"{first_name} {last_name}:\
                \n День разбора: {day:.0f}\
                \n Средняя продуктивность разбора {user_prod:.1f}\n\n"

        await bot.send_message(chat_id=callback_query.from_user.id,
                               text=text_message)
        await bot.delete_message(chat_id=callback_query.from_user.id,
                                 message_id=callback_query.message.message_id)
        await bot.send_message(chat_id=callback_query.from_user.id,
                               text="Ваша продуктивность по дням в сообщении",
                               reply_markup=employee_registed_kb)

    except Exception:
        await bot.delete_message(chat_id=callback_query.from_user.id,
                                 message_id=callback_query.message.message_id)
        await bot.send_message(chat_id=callback_query.from_user.id,
                               text="Что-то пошло не так :(",
                               reply_markup=employee_registed_kb)


@dp.callback_query_handler(text="show_shop_stat")
async def show_shop_stat(
    callback_query: types.CallbackQuery
):
    user_id = callback_query.from_user.id
    shop_id = await check_shop_from_user(user_id)
    list_by_weeks = await check_avg_productivity_employees_in_shop(
        shop_id=shop_id)
    text_message = ''
    try:
        for week in list_by_weeks:
            first_name = week['first_name']
            last_name = week['last_name']
            shop_id = week['shop_id']
            user_prod = week['avg']
            week = week['week_number']
            text_message += f"{first_name} {last_name}:\
                \n Неделя разбора: {week:.0f}\
                \n Средняя продуктивность разбора {user_prod:.1f}\n\n"

        await bot.send_message(chat_id=callback_query.from_user.id,
                               text=f"Магазин: {shop_id}\
                                \n{text_message}")
        await bot.delete_message(chat_id=callback_query.from_user.id,
                                 message_id=callback_query.message.message_id)
        await bot.send_message(chat_id=callback_query.from_user.id,
                               text="Продуктивность сотрудников в сообщении",
                               reply_markup=employee_registed_kb)

    except Exception:
        await bot.delete_message(chat_id=callback_query.from_user.id,
                                 message_id=callback_query.message.message_id)
        await bot.send_message(chat_id=callback_query.from_user.id,
                               text="Что-то пошло не так :(",
                               reply_markup=employee_registed_kb)


@dp.callback_query_handler(text="show_top_in_brand")
async def show_top30_in_brand(
    callback_query: types.CallbackQuery
):
    user_id = callback_query.from_user.id
    brand = await check_brand_from_user(user_id)
    list_by_weeks = await check_top30_in_brand(brand=brand)
    text_message = ''
    n = 1
    try:
        for week in list_by_weeks:
            first_name = week['first_name']
            last_name = week['last_name']
            week_number = week['week_number']
            week_prod = week['week_prod']
            text_message += f"{n}. {first_name} {last_name}\
            \n Cредняя продуктивность разбора {week_prod:.1f}"
            n += 1

        await bot.send_message(chat_id=callback_query.from_user.id,
                               text=f"Неделя: {week_number:.0f}\
                               \n{text_message}")
        await bot.delete_message(chat_id=callback_query.from_user.id,
                                 message_id=callback_query.message.message_id)
        await bot.send_message(chat_id=callback_query.from_user.id,
                               text="Продуктивность сотрудников в сообщении",
                               reply_markup=employee_registed_kb)

    except Exception:
        await bot.delete_message(chat_id=callback_query.from_user.id,
                                 message_id=callback_query.message.message_id)
        await bot.send_message(chat_id=callback_query.from_user.id,
                               text="Что-то пошло не так :(",
                               reply_markup=employee_registed_kb)
