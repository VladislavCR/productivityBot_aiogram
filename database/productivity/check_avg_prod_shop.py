import asyncpg
from config.bot_config import CONFIG_DIR
from dotenv import dotenv_values


config = dotenv_values(CONFIG_DIR / ".env")

USER = config['user']
PSWD = config['password']
DB = config['database']
HOST = config['host']


async def check_avg_productivity_shops():
    conn = await asyncpg.connect(user=USER,
                                 password=PSWD,
                                 database=DB,
                                 host=HOST)
    rows = await conn.fetch(
        'WITH prod_table AS\
        (SELECT AVG(users_productivity.productivity) AS user_prod,\
        users.user_id, users.shop_id\
        FROM users\
        JOIN users_productivity on users.user_id = users_productivity.user_id\
        GROUP BY users.user_id)\
        SELECT shop_id, avg(user_prod) from prod_table\
        GROUP BY shop_id\
        ORDER BY AVG(user_prod) DESC')
    await conn.close()
    if rows is None:
        return 'None'
    else:
        return [dict(row) for row in rows]


async def check_avg_productivity_employees_in_shop(shop_id):
    conn = await asyncpg.connect(user=USER,
                                 password=PSWD,
                                 database=DB,
                                 host=HOST)
    rows = await conn.fetch(
        "WITH prod_table AS\
        (SELECT AVG(users_productivity.productivity) AS user_prod,\
        first_name, last_name,\
        users.user_id, users.shop_id, start_time::date AS date_prod\
        FROM users\
        JOIN users_productivity on users.user_id = users_productivity.user_id\
        WHERE users.shop_id = $1\
        GROUP BY users.user_id, start_time, first_name, last_name)\
        SELECT shop_id, avg(user_prod),\
        date_part('week', date_prod) AS week_number,\
        first_name, last_name from prod_table\
        GROUP BY shop_id, week_number, first_name, last_name\
        ORDER BY AVG(user_prod) DESC", shop_id)
    await conn.close()
    if rows is None:
        return 'None'
    else:
        return [dict(row) for row in rows]
