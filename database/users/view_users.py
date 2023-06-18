import asyncpg
from config.bot_config import CONFIG_DIR
from dotenv import dotenv_values


config = dotenv_values(CONFIG_DIR / '.env')


USER = config['user']
PSWD = config['password']
DB = config['database']
HOST = config['host']


async def get_employees():
    conn = await asyncpg.connect(
        user=USER, password=PSWD, database=DB, host=HOST
    )
    rows = await conn.fetch(
        'SELECT id, user_first_name,user_last_name, user_position FROM user_role'
    )
    await conn.close()
    if rows is None:
        return 'None'
    else:
        return [dict(row) for row in rows]
