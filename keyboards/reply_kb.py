from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

choice_position_kb = ReplyKeyboardMarkup(one_time_keyboard=True,
                                         resize_keyboard=True)

emp_saler = KeyboardButton("Продавец-кассир")
emp_senior_saler = KeyboardButton("Старший продавец")
emp_merch = KeyboardButton("Декоратор")
emp_admin = KeyboardButton("Администратор")
emp_deputy_director = KeyboardButton("Зам. директора")
emp_director = KeyboardButton("Директор")

choice_position_kb.add(
    emp_saler).add(
        emp_senior_saler).add(
            emp_merch).add(
                emp_admin).add(
                    emp_deputy_director).add(
                        emp_director)
