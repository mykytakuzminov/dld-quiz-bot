import os

import asyncpg
from asyncpg import Pool
from dotenv import load_dotenv

load_dotenv()


async def create_pool() -> Pool:
    return await asyncpg.create_pool(os.getenv("ASYNCPG_URL", ""))


async def close_pool(pool: Pool) -> None:
    await pool.close()
