import asyncpg
from config.bot_config import CONFIG_DIR
from dotenv import dotenv_values


config = dotenv_values(CONFIG_DIR / '.env')


USER = config['user']
PSWD = config['password']
DB = config['database']
HOST = config['host']


async def get_shops():
    conn = await asyncpg.connect(
        user=USER, password=PSWD, database=DB, host=HOST
    )
    rows = await conn.fetch(
        'SELECT shop_id, shop_number, brand, city FROM shops'
    )
    await conn.close()
    if rows is None:
        return 'None'
    else:
        return [dict(row) for row in rows]
