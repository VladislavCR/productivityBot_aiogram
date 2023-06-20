import asyncpg
from config.bot_config import CONFIG_DIR
from dotenv import dotenv_values


config = dotenv_values(CONFIG_DIR / ".env")

USER = config['user']
PSWD = config['password']
DB = config['database']
HOST = config['host']


async def create_user_bd(user_id,
                         first_name,
                         last_name,
                         user_position,
                         shop_id):
    conn = await asyncpg.connect(user=USER,
                                 password=PSWD,
                                 database=DB,
                                 host=HOST)
    await conn.execute('''INSERT INTO users (user_id, first_name, last_name, user_position, shop_id) VALUES($1, $2, $3, $4, $5''',
                       user_id, first_name, last_name, user_position, shop_id)
    await conn.close()
