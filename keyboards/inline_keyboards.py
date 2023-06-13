from aiogram import types


admin_panel_main_menu = types.InlineKeyboardMarkup()

appoint_admin = types.InlineKeyboardButton(
    text="Назначить права админа", callback_data="appoint_admin"
)
add_shop = types.InlineKeyboardButton(
    text="Добавить магазин", callback_data="add_shop"
)
remove_admin = types.InlineKeyboardButton(
    text="Убрать права админа", callback_data="remove_admin"
)
# secret_button = types.InlineKeyboardButton(
#     text="Секретная кнопка", callback_data="secret"
# )


admin_panel_main_menu.add(appoint_admin, remove_admin).add(add_shop)


director_panel_main_menu = types.InlineKeyboardMarkup()

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

director_panel_main_menu.add(view_staff_list).add(add_staff, remove_staff)
director_panel_main_menu.add(raiting_inside_store).add(raiting_of_store)
director_panel_main_menu.add(statistic_by_day).add(type_of_operation)


staff_pannel_main_menu = types.InlineKeyboardMarkup()

raiting_inside_store = types.InlineKeyboardButton(
    text="Посмотреть рейтинг сотрудников внутри магизна",
    callback_data="raiting_inside_store"
)
statistic_by_day = types.InlineKeyboardButton(
    text="Посмотреть статистику по дням",
    callback_data="statistic_by_day"
)

staff_pannel_main_menu.add(raiting_inside_store).add(statistic_by_day)
