from aiogram import types

employee_kb_registration = types.InlineKeyboardMarkup()

start_reg = types.InlineKeyboardButton(
    text="Начать регистрацию", callback_data="start_reg")

help_new_emp = types.InlineKeyboardButton(
    text="Помощь",
    callback_data="help_new_emp")

employee_kb_registration.add(start_reg).add(help_new_emp)


employee_kb_return = types.InlineKeyboardMarkup()

return_bt = types.InlineKeyboardButton(
    text="Вернутся в главное меню",
    callback_data="start_reg")

employee_kb_return.add(return_bt)


employee_registed_kb = types.InlineKeyboardMarkup(row_width=1)

show_personal_stat_month = types.InlineKeyboardButton(
    text="Посмотреть персональную статистику по неделям",
    callback_data="show_personal_stat_week")

show_personal_stat_day = types.InlineKeyboardButton(
    text="Посмотреть персональную статистику по дням",
    callback_data="show_personal_stat_day")

show_shop_stat = types.InlineKeyboardButton(
    text="Посмотреть статистику магазина по неделям",
    callback_data="show_shop_stat")

show_all_stat = types.InlineKeyboardButton(
    text="Посмореть ТОП 30 лучших сотрудников бренда",
    callback_data="show_top_in_brand")

employee_registed_kb.add(show_personal_stat_month,
                         show_personal_stat_day,
                         show_shop_stat,
                         show_all_stat)
