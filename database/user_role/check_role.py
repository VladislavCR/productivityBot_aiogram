import asyncpg
from config.bot_config import CONFIG_DIR
from dotenv import dotenv_values


config = dotenv_values(CONFIG_DIR / '.env')


USER = config['user']
PSWD = config['password']
DB = config['database']
HOST = config['host']


async def check_bd_user_role(user_id):
    conn = await asyncpg.connect(
        user=USER, password=PSWD, database=DB, host=HOST
    )
    row = await conn.fetchrow(
        'SELECT user_role FROM users_role WHERE user_id = $1',
        user_id,
    )
    await conn.close()
    if row is None:
        return 'None'
    else:
        return row['user_role']


async def check_user(user_id):
    conn = await asyncpg.connect(
        user=USER, password=PSWD, database=DB, host=HOST
    )
    row = await conn.fetchrow(
        'SELECT user_id FROM users WHERE user_id = $1',
        user_id,
    )
    await conn.close()
    if row is None:
        return False
    else:
        return True
