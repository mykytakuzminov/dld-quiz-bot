from datetime import datetime, timezone

from asyncpg import Pool

from dld_quiz_bot.db.models import Question, User
from dld_quiz_bot.enums import GermanLand


async def create_user(
    pool: Pool,
    telegram_id: int,
    username: str | None,
    selected_land: GermanLand,
) -> None:
    query = """
        INSERT INTO users (telegram_id, username, selected_land, created_at)
        VALUES ($1, $2, $3, $4)
    """

    created_at = datetime.now(timezone.utc)

    await pool.execute(query, telegram_id, username, selected_land.value, created_at)


async def get_user(pool: Pool, telegram_id: int) -> User | None:
    query = """
        SELECT * FROM users WHERE telegram_id = $1
    """

    user = await pool.fetchrow(query, telegram_id)

    if user is None:
        return None

    return User.from_record(user)


async def change_user_land(pool: Pool, telegram_id: int, new_land: GermanLand) -> None:
    query = """
        UPDATE users SET selected_land = $1 WHERE telegram_id = $2
    """

    await pool.execute(query, new_land.value, telegram_id)


async def get_random_question(pool: Pool, telegram_id: int) -> Question | None:
    user = await get_user(pool, telegram_id)

    if user is None:
        return None

    query = """
        SELECT * FROM questions WHERE land IS NULL OR land = $1 ORDER BY RANDOM() LIMIT 1
    """

    question = await pool.fetchrow(query, user.selected_land.value)

    if question is None:
        return None

    return Question.from_record(question)


async def get_general_questions(pool: Pool, limit: int = 23) -> list[Question]:
    query = """
        SELECT * FROM questions WHERE land IS NULL ORDER BY RANDOM() LIMIT $1
    """

    questions = await pool.fetch(query, limit)

    if questions is None:
        return []

    return [Question.from_record(question) for question in questions]


async def get_land_questions(pool: Pool, telegram_id: int, limit: int = 10) -> list[Question]:
    user = await get_user(pool, telegram_id)

    if user is None:
        return []

    query = """
        SELECT * FROM questions WHERE land = $1 ORDER BY RANDOM() LIMIT $2
    """

    questions = await pool.fetch(query, user.selected_land.value, limit)

    return [Question.from_record(question) for question in questions]


async def create_exam_record(pool: Pool, telegram_id: int, correct_answers: int) -> None:
    query = """
        INSERT INTO exam_sessions (user_id, correct_answers)
        VALUES ($1, $2)
    """

    await pool.execute(query, telegram_id, correct_answers)
