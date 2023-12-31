import asyncpg
from config.bot_config import CONFIG_DIR
from dotenv import dotenv_values


config = dotenv_values(CONFIG_DIR / '.env')


USER = config['user']
PSWD = config['password']
DB = config['database']
HOST = config['host']


async def check_shop(shop_id):
    conn = await asyncpg.connect(
        user=USER, password=PSWD, database=DB, host=HOST
    )
    row = await conn.fetchrow(
        'SELECT shop_id FROM shops WHERE shop_id = $1',
        shop_id,
    )
    await conn.close()
    if row is None:
        return False
    else:
        return True
