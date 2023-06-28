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
