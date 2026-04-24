from datetime import datetime, timezone

from asyncpg import Pool

from dld_quiz_bot.db.models import User


async def create_user(
    pool: Pool,
    telegram_id: int,
    username: str | None,
    selected_land: str,
) -> None:
    query = """
        INSERT INTO users (telegram_id, username, selected_land, created_at)
        VALUES ($1, $2, $3, $4)
    """

    created_at = datetime.now(timezone.utc)

    await pool.execute(query, telegram_id, username, selected_land, created_at)


async def get_user(pool: Pool, telegram_id: int) -> User | None:
    query = """
        SELECT * FROM users WHERE telegram_id = $1
    """

    record = await pool.fetchrow(query, telegram_id)

    if record is None:
        return None

    return User(
        telegram_id=record["telegram_id"],
        username=record["username"],
        selected_land=record["selected_land"],
        created_at=record["created_at"],
    )


async def change_user_land(pool: Pool, telegram_id: int, new_land: str) -> None:
    query = """
        UPDATE users SET selected_land = $1 WHERE telegram_id = $2
    """

    await pool.execute(query, new_land, telegram_id)
