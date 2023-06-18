import asyncpg
from config.bot_config import CONFIG_DIR
from dotenv import dotenv_values


config = dotenv_values(CONFIG_DIR / ".env")

USER = config['user']
PSWD = config['password']
DB = config['database']
HOST = config['host']


async def change_users_bd(id,
                          user_role,
                          user_first_name,
                          user_last_name,
                          user_position):
    conn = await asyncpg.connect(user=USER,
                                 password=PSWD,
                                 database=DB,
                                 host=HOST)
    await conn.execute(f"UPDATE user_role SET user_role=$1, user_first_name=$2, user_last_name=$3 WHERE id=$4",
                       user_role,
                       user_first_name,
                       user_last_name,
                       user_position)
    await conn.close()
