import asyncpg
from config.bot_config import CONFIG_DIR
from dotenv import dotenv_values


config = dotenv_values(CONFIG_DIR / ".env")

USER = config['user']
PSWD = config['password']
DB = config['database']
HOST = config['host']


async def create_shop_cr_bd(shop_id, city):
    conn = await asyncpg.connect(user=USER,
                                 password=PSWD,
                                 database=DB,
                                 host=HOST)
    await conn.execute('INSERT INTO shops (shop_id, brand, city) VALUES($1, $2, $3',
                       shop_id, 'CR', city)
    await conn.close()


async def create_shop_re_bd(shop_id, city):
    conn = await asyncpg.connect(user=USER,
                                 password=PSWD,
                                 database=DB,
                                 host=HOST)
    await conn.execute('INSERT INTO shops (shop_id, brand, city) VALUES($1, $2, $3',
                       shop_id, 'RE', city)
    await conn.close()


async def create_shop_sin_bd(shop_id, city):
    conn = await asyncpg.connect(user=USER,
                                 password=PSWD,
                                 database=DB,
                                 host=HOST)
    await conn.execute('INSERT INTO shops (shop_id, brand, city) VALUES($1, $2, $3',
                       shop_id, 'SIN', city)
    await conn.close()


async def create_shop_xc_bd(shop_id, city):
    conn = await asyncpg.connect(user=USER,
                                 password=PSWD,
                                 database=DB,
                                 host=HOST)
    await conn.execute('INSERT INTO shops (shop_id, brand, city) VALUES($1, $2, $3',
                       shop_id, 'XC', city)
    await conn.close()


async def create_shop_mo_bd(shop_id, city):
    conn = await asyncpg.connect(user=USER,
                                 password=PSWD,
                                 database=DB,
                                 host=HOST)
    await conn.execute('INSERT INTO shops (shop_id, brand, city) VALUES($1, $2, $3',
                       shop_id, 'MO', city)
    await conn.close()
