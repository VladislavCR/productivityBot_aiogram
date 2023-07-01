from aiogram import types

employee_kb_registration = types.InlineKeyboardMarkup()

start_reg = types.InlineKeyboardButton(
    text="Начать регистрацию", callback_data="start_reg")

employee_kb_registration.add(start_reg)


employee_kb_return = types.InlineKeyboardMarkup()

return_bt = types.InlineKeyboardButton(
    text="Вернуться в главное меню",
    callback_data="start_reg")

employee_kb_return.add(return_bt)


employee_registed_kb = types.InlineKeyboardMarkup(row_width=1)

show_personal_stat_month = types.InlineKeyboardButton(
    text="Ваша продуктивность по неделям",
    callback_data="show_personal_stat_week")

show_personal_stat_day = types.InlineKeyboardButton(
    text="Ваша продуктивность по дням",
    callback_data="show_personal_stat_day")

show_shop_stat = types.InlineKeyboardButton(
    text="Продуктивность сотрудников магазина по неделям",
    callback_data="show_shop_stat")

show_all_stat = types.InlineKeyboardButton(
    text="30 лучших сотрудников бренда",
    callback_data="show_top_in_brand")

employee_registed_kb.add(show_personal_stat_month,
                         show_personal_stat_day,
                         show_shop_stat,
                         show_all_stat)
