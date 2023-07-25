from aiogram import types

director_kb_main_menu = types.InlineKeyboardMarkup(row_width=1)

view_staff_list = types.InlineKeyboardButton(
    text="Посмотреть список сотрудников",
    callback_data="view_list"
)
remove_employee = types.InlineKeyboardButton(
    text="Удалить уволенного сотрудника",
    callback_data="remove_employee"
)
raiting_of_store = types.InlineKeyboardButton(
    text="Просмотреть общий рейтинг среди магазинов",
    callback_data="raiting_of_store"
)
raiting_inside_store = types.InlineKeyboardButton(
    text="Рейтинг сотрудников внутри магазина",
    callback_data="raiting_inside_store"
)
statistic_by_day = types.InlineKeyboardButton(
    text="Статистика по дням в магазине",
    callback_data="statistic_by_day"
)
type_of_operation = types.InlineKeyboardButton(
    text="Подсчет продуктивности",
    callback_data="type_of_operation"
)

director_kb_main_menu.add(view_staff_list,
                          remove_employee,
                          raiting_inside_store,
                          raiting_of_store,
                          statistic_by_day,
                          type_of_operation)

director_kb_operations = types.InlineKeyboardMarkup(row_width=1)

analysis_of_delivery = types.InlineKeyboardButton(
    text="Продуктивность разбора поставки",
    callback_data="analysis_of_delivery"
)
transfer_of_delivery = types.InlineKeyboardButton(
    text="", callback_data="analysis_of_delivery"
)
transfer_to_salesfloor = types.InlineKeyboardButton(
    text="СКОРО.Продуктивность выдачи вещей в торговый зал",
    callback_data="transfer_to_salesfloor"
)
transfer_to_warehouse = types.InlineKeyboardButton(
    text="СКОРО.Продуктивность разноса поставки по складу",
    callback_data="transfer_to_warehouse"
)
revaluation_of_salesfloor = types.InlineKeyboardButton(
    text="СКОРО.Переоценка торгового зала",
    callback_data="revaluation_of_salesfloor"
)
back_to_main_menu = types.InlineKeyboardButton(
    text="Вернуться в главное меню",
    callback_data="dir_back_to_main_menu"
)

director_kb_operations.add(analysis_of_delivery,
                           transfer_of_delivery,
                           transfer_to_salesfloor,
                           transfer_to_warehouse,
                           revaluation_of_salesfloor,
                           back_to_main_menu)
