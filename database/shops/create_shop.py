import asyncpg
from config.bot_config import CONFIG_DIR
from dotenv import dotenv_values


config = dotenv_values(CONFIG_DIR / ".env")

USER = config['user']
PSWD = config['password']
DB = config['database']
HOST = config['host']


async def create_shop_bd(shop_id,
                         shop_number,
                         brand,
                         city):
    conn = await asyncpg.connect(user=USER,
                                 password=PSWD,
                                 database=DB,
                                 host=HOST)
    await conn.execute('''INSERT INTO shops (shop_id, shop_number, brand, city) VALUES($1, $2, $3, $4''',
                       shop_id, shop_number, brand, city)
    await conn.close()
