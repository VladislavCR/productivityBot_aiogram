import asyncpg
from config.bot_config import CONFIG_DIR
from dotenv import dotenv_values


config = dotenv_values(CONFIG_DIR / ".env")

USER = config['user']
PSWD = config['password']
DB = config['database']
HOST = config['host']


async def check_avg_productivity_by_day(shop_id):
    conn = await asyncpg.connect(user=USER,
                                 password=PSWD,
                                 database=DB,
                                 host=HOST)
    rows = await conn.fetch(
        'WITH prod_table AS\
        (SELECT AVG(users_productivity.productivity) AS user_prod,\
        users_productivity.user_id, start_time::date, shops.shop_id\
        FROM users_productivity\
        JOIN users ON users.user_id = users_productivity.user_id\
        JOIN shops ON  users.shop_id = shops.shop_id\
        WHERE shops.shop_id = $1\
        GROUP BY shops.shop_id, users_productivity.user_id,\
        users_productivity.start_time)\
        SELECT start_time, avg(user_prod) from prod_table\
        GROUP BY start_time\
        ORDER BY start_time DESC', shop_id)
    await conn.close()
    if rows is None:
        return 'None'
    else:
        return [dict(row) for row in rows]


async def check_personal_prod_by_day(user_id):
    conn = await asyncpg.connect(user=USER,
                                 password=PSWD,
                                 database=DB,
                                 host=HOST)
    rows = await conn.fetch(
        "WITH prod_table AS\
        (SELECT first_name, last_name, start_time::date AS date_prod,\
        AVG(users_productivity.productivity) AS user_prod\
        FROM users_productivity\
        JOIN users on users.user_id = users_productivity.user_id\
        WHERE users.user_id = $1\
        GROUP BY users.first_name, users.last_name, date_prod)\
        SELECT date_part('day', date_prod) AS day_number,\
        first_name, last_name, user_prod\
        FROM prod_table", user_id)
    await conn.close()
    if rows is None:
        return 'None'
    else:
        return [dict(row) for row in rows]
