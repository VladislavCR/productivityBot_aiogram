import asyncpg
from config.bot_config import CONFIG_DIR
from dotenv import dotenv_values


config = dotenv_values(CONFIG_DIR / '.env')


USER = config['user']
PSWD = config['password']
DB = config['database']
HOST = config['host']


async def get_employees(shop_id):
    conn = await asyncpg.connect(
        user=USER, password=PSWD, database=DB, host=HOST
    )
    rows = await conn.fetch(
        'SELECT user_id, first_name, last_name, user_position\
        FROM users WHERE shop_id = $1',
        shop_id
    )
    await conn.close()
    if rows is None:
        return 'None'
    else:
        return [dict(row) for row in rows]


async def get_shop(user_id):
    conn = await asyncpg.connect(
        user=USER, password=PSWD, database=DB, host=HOST
    )
    row = await conn.fetch(
        'SELECT shop_id FROM users where user_id = $1', user_id
    )
    await conn.close()

    return row[0]


async def get_employee_from_users(user_id):
    conn = await asyncpg.connect(
        user=USER, password=PSWD, database=DB, host=HOST
    )
    rows = await conn.fetch(
        'SELECT first_name, last_name, user_position\
        FROM users WHERE user_id = $1',
        user_id
    )
    await conn.close()
    if rows is None:
        return 'None'
    else:
        return rows[0]
