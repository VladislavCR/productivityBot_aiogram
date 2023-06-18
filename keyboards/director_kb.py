from aiogram import types

director_kb_main_menu = types.InlineKeyboardMarkup()

view_staff_list = types.InlineKeyboardButton(
    text="Посмотреть список сотрудников", callback_data="view_list"
)
add_staff = types.InlineKeyboardButton(
    text="Добавить сотрудника", callback_data="add_staff"
)
remove_staff = types.InlineKeyboardButton(
    text="Убрать сотрудника", callback_data="remove_staff"
)
raiting_of_store = types.InlineKeyboardButton(
    text="Просмотреть общий рейтинг магазина", callback_data="raiting_of_store"
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

director_kb_main_menu.add(view_staff_list).add(add_staff, remove_staff)
director_kb_main_menu.add(raiting_inside_store).add(raiting_of_store)
director_kb_main_menu.add(statistic_by_day).add(type_of_operation)
