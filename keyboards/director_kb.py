from aiogram import types

director_kb_main_menu = types.InlineKeyboardMarkup()

view_staff_list = types.InlineKeyboardButton(
    text="Посмотреть список сотрудников",
    callback_data="view_list"
)
add_employee = types.InlineKeyboardButton(
    text="Добавить сотрудника",
    callback_data="add_employee"
)
remove_employee = types.InlineKeyboardButton(
    text="Удалить сотрудника",
    callback_data="remove_employee"
)
raiting_of_store = types.InlineKeyboardButton(
    text="Просмотреть общий рейтинг магазина",
    callback_data="raiting_of_store"
)
raiting_inside_store = types.InlineKeyboardButton(
    text="Посмотреть рейтинг сотрудников внутри магизна",
    callback_data="raiting_inside_store"
)
statistic_by_day = types.InlineKeyboardButton(
    text="Посмотреть статистику по дням",
    callback_data="statistic_by_day"
)
type_of_operation = types.InlineKeyboardButton(
    text="Выбрать процесс для подсчета продуктивности",
    callback_data="type_of_operation"
)

director_kb_main_menu.add(view_staff_list).add(add_employee, remove_employee)
director_kb_main_menu.add(raiting_inside_store).add(raiting_of_store)
director_kb_main_menu.add(statistic_by_day).add(type_of_operation)


director_kb_operations = types.InlineKeyboardMarkup(row_width=1)

analysis_of_delivery = types.InlineKeyboardButton(
    text="Продуктивность разбора поставки",
    callback_data="analysis_of_delivery"
)
transfer_of_delivery = types.InlineKeyboardButton(
    text="", callback_data="analysis_of_delivery"
)
transfer_to_salesfloor = types.InlineKeyboardButton(
    text="Продуктивность выдачи вещей в торговый зал",
    callback_data="transfer_to_salesfloor"
)
transfer_to_warehouse = types.InlineKeyboardButton(
    text="Продуктивность разноса поставки по складу",
    callback_data="transfer_to_warehouse"
)
revaluation_of_salesfloor = types.InlineKeyboardButton(
    text="Переоценка торгового зала",
    callback_data="revaluation_of_salesfloor"
)

director_kb_operations.add(analysis_of_delivery,
                           transfer_of_delivery,
                           transfer_to_salesfloor,
                           transfer_to_warehouse,
                           revaluation_of_salesfloor)


director_kb_stop_productivitty = types.InlineKeyboardMarkup()

stop_button_prod = types.InlineKeyboardButton(
    text="Остановить подсчет продуктивности",
    callback_data="stop_productivity"
)

director_kb_stop_productivitty.add(stop_button_prod)
