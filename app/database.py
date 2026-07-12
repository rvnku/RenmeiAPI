import aiosqlite
from app.env import Env


database_path = Env.database_url.replace('sqlite:///', '')


async def get_database():
    async with aiosqlite.connect(database_path) as database:
        yield database

async def init_database():
    async with aiosqlite.connect(database_path) as database:
        await database.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id TEXT PRIMARY KEY,
                access_token TEXT NOT NULL,
                refresh_token TEXT,
                expires_at TIMESTAMP NOT NULL
            )
        ''')
        await database.commit()
