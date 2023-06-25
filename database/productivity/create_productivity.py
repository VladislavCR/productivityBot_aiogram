import asyncpg
from config.bot_config import CONFIG_DIR
from dotenv import dotenv_values


config = dotenv_values(CONFIG_DIR / ".env")

USER = config['user']
PSWD = config['password']
DB = config['database']
HOST = config['host']


async def create_productivity(user_id, start_time, end_time, num_of_units, productivity):
    conn = await asyncpg.connect(user=USER,
                                 password=PSWD,
                                 database=DB,
                                 host=HOST)
    await conn.execute('INSERT INTO users_productivity (user_id, start_time, end_time, num_of_units, productivity) VALUES($1, $2, $3, $4, $5)',
                       user_id, start_time, end_time, num_of_units, productivity)
    await conn.close()
