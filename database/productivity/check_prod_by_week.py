import asyncpg
from config.bot_config import CONFIG_DIR
from dotenv import dotenv_values


config = dotenv_values(CONFIG_DIR / ".env")

USER = config['user']
PSWD = config['password']
DB = config['database']
HOST = config['host']


async def check_personal_prod_by_week(user_id):
    conn = await asyncpg.connect(user=USER,
                                 password=PSWD,
                                 database=DB,
                                 host=HOST)
    rows = await conn.fetch(
        "WITH prod_table AS\
        (SELECT first_name, last_name, start_time::date AS date_week,\
        AVG(users_productivity.productivity) AS user_prod\
        FROM users_productivity\
        JOIN users on users.user_id = users_productivity.user_id\
        WHERE users.user_id = $1\
        GROUP BY users.first_name, users.last_name, date_week)\
        SELECT date_part('week', date_week) AS week_number,\
        first_name, last_name, AVG(user_prod)\
        FROM prod_table\
        GROUP BY week_number, first_name, last_name", user_id)
    await conn.close()
    if rows is None:
        return 'None'
    else:
        return [dict(row) for row in rows]


async def check_top30_in_brand(user_id, brand):
    conn = await asyncpg.connect(user=USER,
                                 password=PSWD,
                                 database=DB,
                                 host=HOST)
    rows = await conn.fetch(
        "WITH prod_table AS\
        (SELECT first_name, last_name, start_time::date AS date_week,\
        AVG(users_productivity.productivity) AS user_prod\
        FROM users_productivity\
        JOIN users ON users.user_id = users_productivity.user_id\
        join shops ON users.shop_id  = shops.shop_id\
        WHERE users.user_id = $1 and brand = $2\
        GROUP BY users.first_name, users.last_name, date_week)\
        SELECT date_part('week', date_week) AS week_number,\
        first_name, last_name, AVG(user_prod) AS week_prod\
        FROM prod_table\
        GROUP BY week_number, first_name, last_name\
        ORDER BY week_prod desc\
        LIMIT 30", user_id, brand)
    await conn.close()
    if rows is None:
        return 'None'
    else:
        return [dict(row) for row in rows]
