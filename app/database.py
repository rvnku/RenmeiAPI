import aiosqlite
from app.config import DATABASE_URL


DATABASE_PATH = DATABASE_URL.replace('sqlite:///', '')


async def get_database():
    async with aiosqlite.connect(DATABASE_PATH) as database:
        yield database

async def init_database():
    async with aiosqlite.connect(DATABASE_PATH) as database:
        await database.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id TEXT PRIMARY KEY,
                access_token TEXT NOT NULL,
                refresh_token TEXT,
                expires_at TIMESTAMP NOT NULL
            )
        ''')
        await database.commit()
