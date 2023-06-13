import asyncpg
from config.bot_config import CONFIG_DIR
from dotenv import dotenv_values


config = dotenv_values(CONFIG_DIR / '.env')


USER = config['user']
PSWD = config['password']
DB = config['database']
HOST = config['host']


async def check_bd_user_role(id):
    conn = await asyncpg.connect(
        user=USER, password=PSWD, database=DB, host=HOST
    )
    row = await conn.fetchrow(
        'SELECT user_role FROM user_role WHERE id = $1',
        id,
    )
    await conn.close()
    if row is None:
        return 'None'
    else:
        return row['user_role']
