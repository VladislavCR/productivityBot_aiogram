import asyncpg
from config.bot_config import CONFIG_DIR
from dotenv import dotenv_values


config = dotenv_values(CONFIG_DIR / ".env")

USER = config['user']
PSWD = config['password']
DB = config['database']
HOST = config['host']


async def check_avg_productivity_shop():
    conn = await asyncpg.connect(user=USER,
                                 password=PSWD,
                                 database=DB,
                                 host=HOST)
    rows = await conn.fetch(
        'WITH prod_table AS\
        (SELECT AVG(users_productivity.productivity) AS user_prod,\
        users.user_id, shops.shop_id\
        FROM users\
        JOIN users_productivity on users.user_id = users_productivity.user_id\
        JOIN shops on users.shop_id = shops.shop_id\
        GROUP BY shops.shop_id, users.user_id)\
        SELECT shop_id, avg(user_prod) from prod_table\
        GROUP BY shop_id\
        ORDER BY AVG(user_prod) DESC')
    await conn.close()
    if rows is None:
        return 'None'
    else:
        return [dict(row) for row in rows]
