from os import getenv

import pytest
from alembic.config import Config
from dotenv import load_dotenv

from alembic import command
from dld_quiz_bot.db.database import close_pool, create_pool

load_dotenv()

DATABASE = getenv("TEST_DATABASE_URL")
POOL = getenv("TEST_ASYNCPG_URL")


def run_migrations():
    if DATABASE is None:
        raise ValueError("TEST_DATABASE_URL is not set")
    if POOL is None:
        raise ValueError("TEST_ASYNCPG_URL is not set")

    alembic_cfg = Config("alembic.ini")
    alembic_cfg.set_main_option("sqlalchemy.url", DATABASE)
    command.upgrade(alembic_cfg, "head")


run_migrations()


@pytest.fixture
async def pool():
    pool = await create_pool(POOL)
    yield pool
    await close_pool(pool)


@pytest.fixture(autouse=True)
async def clean_db(pool):
    yield
    await pool.execute("DELETE FROM exam_sessions")
    await pool.execute("DELETE FROM users")
    await pool.execute("DELETE FROM questions")
