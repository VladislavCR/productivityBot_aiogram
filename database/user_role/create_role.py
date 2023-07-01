import asyncpg
from config.bot_config import CONFIG_DIR
from dotenv import dotenv_values


config = dotenv_values(CONFIG_DIR / '.env')


user = str(config['user'])
password = str(config['password'])
database = str(config['database'])
host = str(config['host'])


# Даем права админа сотруднику
async def create_admin(user_id):
    conn = await asyncpg.connect(
        user=user, password=password, database=database, host=host
    )
    await conn.execute("UPDATE users_role\
                       SET user_role = $2\
                       WHERE user_id = $1", user_id, 'admin')
    await conn.close()


# Даем права директора сотруднику
async def create_director(user_id):
    conn = await asyncpg.connect(
        user=user, password=password, database=database, host=host
    )
    await conn.execute("UPDATE users_role\
                       SET user_role = $2\
                       WHERE user_id = $1", user_id, 'director')
    await conn.close()


# Создаем роль пользователя
async def create_user(user_id):
    conn = await asyncpg.connect(
        user=user, password=password, database=database, host=host
    )
    await conn.execute("INSERT INTO users_role(user_id, user_role) VALUES($1, $2)",
                       user_id,
                       'employee')
    await conn.close()


# Удаляем любую роль пользователя
async def delete_user(user_id):
    conn = await asyncpg.connect(
        user=user, password=password, database=database, host=host
    )
    await conn.execute("DELETE FROM users_role WHERE user_id = $1", user_id)
    await conn.close()
