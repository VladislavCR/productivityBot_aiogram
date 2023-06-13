from aiogram import types


admin_panel_main_menu = types.InlineKeyboardMarkup()

button1 = types.InlineKeyboardButton(text="Посмотреть список сотрудников",
                                     callback_data="view_list")
button2 = types.InlineKeyboardButton(text="Редактировать список",
                                     callback_data="edit_list")
button3 = types.InlineKeyboardButton(text="Назначить права админа",
                                     callback_data="assign_role")
button4 = types.InlineKeyboardButton(text="Секретная кнопка",
                                     callback_data="secret")
admin = types.InlineKeyboardButton(text="Админ",
                                   callback_data='take_user_role')

admin_panel_main_menu.add(button1).add(button2, button3).add(button4).add(admin)
