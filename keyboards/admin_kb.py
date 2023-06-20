from aiogram import types


admin_kb_main_menu = types.InlineKeyboardMarkup()

make_user_admin = types.InlineKeyboardButton(
    text="Назначить права", callback_data="add_rights"
)
add_shop = types.InlineKeyboardButton(
    text="Добавить магазин", callback_data="add_shop"
)
delete_role_admin = types.InlineKeyboardButton(
    text="Убрать права админа", callback_data="remove_rights"
)

admin_kb_main_menu.add(make_user_admin, delete_role_admin).add(add_shop)


admin_kb_add_rights = types.InlineKeyboardMarkup()

make_user_admin = types.InlineKeyboardButton(
    text="Назначить права администартора", callback_data="make_user_admin"
)
make_user_director = types.InlineKeyboardButton(
    text="Назначить права директора", callback_data="make_user_director"
)
go_back_main_menu = types.InlineKeyboardButton(
    text="Вернуться в главное меню", callback_data="go_back_main_menu"
)

admin_kb_add_rights.add(
    make_user_admin).add(
        make_user_director).add(
            go_back_main_menu)


admin_kb_add_shop = types.InlineKeyboardMarkup()

cr_button = types.InlineKeyboardButton(
    text="Добавить магазин CR", callback_data="add_CR"
)
sin_button = types.InlineKeyboardButton(
    text="Добавить магазин SIN", callback_data="add_SIN"
)
re_button = types.InlineKeyboardButton(
    text="Добавить магазин RE", callback_data="add_RE"
)
mo_button = types.InlineKeyboardButton(
    text="Добавить магазин MO", callback_data="add_MO"
)
xc_button = types.InlineKeyboardButton(
    text="Добавить магаин XC", callback_data="add_XC"
)
go_back_main_menu = types.InlineKeyboardButton(
    text="Вернуться в главное меню", callback_data="go_back_main_menu"
)

admin_kb_add_shop.add(
    sin_button).add(
        re_button).add(
            cr_button).add(
                xc_button).add(
                    mo_button).add(
                        go_back_main_menu)


admin_kb_cr = types.InlineKeyboardMarkup()
add_shop = types.InlineKeyboardButton(
    text="Добавить магазин", callback_data="add_shop_cr"
)
remove_shop = types.InlineKeyboardButton(
    text="Убрать магазин", callback_data="remove_shop_cr"
)
go_back_main_menu = types.InlineKeyboardButton(
    text="Вернуться в главное меню", callback_data="go_back_main_menu"
)

admin_kb_cr.add(add_shop).add(remove_shop).add(go_back_main_menu)

admin_kb_sin = types.InlineKeyboardMarkup()
add_shop = types.InlineKeyboardButton(
    text="Добавить магазин", callback_data="add_shop_sin"
)
remove_staff = types.InlineKeyboardButton(
    text="Убрать магазин", callback_data="remove_shop_sin"
)
go_back_main_menu = types.InlineKeyboardButton(
    text="Вернуться в главное меню", callback_data="go_back_main_menu"
)

admin_kb_sin.add(add_shop).add(remove_staff).add(go_back_main_menu)


admin_kb_re = types.InlineKeyboardMarkup()
add_shop = types.InlineKeyboardButton(
    text="Добавить магазин", callback_data="add_shop_re"
)
remove_staff = types.InlineKeyboardButton(
    text="Убрать магазин", callback_data="remove_shop_re"
)
go_back_main_menu = types.InlineKeyboardButton(
    text="Вернуться в главное меню", callback_data="go_back_main_menu"
)

admin_kb_re.add(add_shop).add(remove_staff).add(go_back_main_menu)


admin_kb_mo = types.InlineKeyboardMarkup()
add_shop = types.InlineKeyboardButton(
    text="Добавить магазин", callback_data="add_shop_mo"
)
remove_staff = types.InlineKeyboardButton(
    text="Убрать магазин", callback_data="remove_shop_mo"
)
go_back_main_menu = types.InlineKeyboardButton(
    text="Вернуться в главное меню", callback_data="go_back_main_menu"
)

admin_kb_mo.add(add_shop).add(remove_staff).add(go_back_main_menu)


admin_kb_xc = types.InlineKeyboardMarkup()
add_shop = types.InlineKeyboardButton(
    text="Добавить магазин", callback_data="add_shop_xc"
)
remove_staff = types.InlineKeyboardButton(
    text="Убрать магазин", callback_data="remove_shop_xc"
)
go_back_main_menu = types.InlineKeyboardButton(
    text="Вернуться в главное меню", callback_data="go_back_main_menu"
)

admin_kb_xc.add(add_shop).add(remove_staff).add(go_back_main_menu)
