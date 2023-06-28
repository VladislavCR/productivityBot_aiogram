import asyncpg
from config.bot_config import CONFIG_DIR
from dotenv import dotenv_values


config = dotenv_values(CONFIG_DIR / ".env")

USER = config['user']
PSWD = config['password']
DB = config['database']
HOST = config['host']


async def check_avg_productivity_users_in_shop(shop_id):
    conn = await asyncpg.connect(user=USER,
                                 password=PSWD,
                                 database=DB,
                                 host=HOST)
    rows = await conn.fetch(
        'SELECT AVG(users_productivity.productivity) AS user_prod,\
        first_name, last_name, users.shop_id\
        FROM users\
        JOIN users_productivity ON users.user_id = users_productivity.user_id\
        WHERE shop_id = $1\
        GROUP BY users.user_id', shop_id)

    await conn.close()
    if rows is None:
        return 'None'
    else:
        return [dict(row) for row in rows]
