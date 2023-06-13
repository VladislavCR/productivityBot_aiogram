import asyncpg
from config.bot_config import CONFIG_DIR
from dotenv import dotenv_values


config = dotenv_values(CONFIG_DIR / '.env')


user = str(config['user'])
password = str(config['password'])
database = str(config['database'])
host = str(config['host'])


# Создаем роль администратора
async def create_admin(id, user_first_name, user_last_name, user_position):
    conn = await asyncpg.connect(
        user=user, password=password, database=database, host=host
    )
    await conn.execute('''INSERT INTO user_role(id, user_role, user_first_name, user_last_name, user_position) VALUES($1,$2,$3,$4,$5)''',
                       id,
                       'admin',
                       user_first_name,
                       user_last_name,
                       user_position,
                       )
    await conn.close()


# Создаем роль пользователя
async def create_user(id, user_first_name, user_last_name, user_position):
    conn = await asyncpg.connect(
        user=user, password=password, database=database, host=host
    )
    await conn.execute('''INSERT INTO user_role(id, user_role, user_first_name, user_last_name, user_position) VALUES($1,$2,$3,$4,$5)''',
                       id,
                       'user',
                       user_first_name,
                       user_last_name,
                       user_position,
                       )
    await conn.close()


# Удаляем любую роль пользователя
async def delete_user(id):
    conn = await asyncpg.connect(
        user=user, password=password, database=database, host=host
    )
    await conn.execute('''DELETE FROM user_role WHERE id = $1''', id)
    await conn.close()
