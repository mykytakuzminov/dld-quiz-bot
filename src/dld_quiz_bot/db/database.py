import asyncpg
from asyncpg import Pool


async def create_pool(url: str) -> Pool:
    return await asyncpg.create_pool(url)


async def close_pool(pool: Pool) -> None:
    await pool.close()
