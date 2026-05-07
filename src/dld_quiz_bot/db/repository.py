from datetime import datetime, timezone

from asyncpg import Pool

from dld_quiz_bot.db.models import ExamSession, Question, User
from dld_quiz_bot.enums import GermanLand

EXAM_TOTAL = 33
EXAM_GENERAL = 23
EXAM_LAND = 10


async def create_user(
    pool: Pool,
    telegram_id: int,
    username: str | None,
    selected_land: GermanLand,
) -> None:
    query = """
        INSERT INTO users (telegram_id, username, selected_land, created_at)
        VALUES ($1, $2, $3, $4)
        ON CONFLICT DO NOTHING
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


async def get_random_question(pool: Pool, land: GermanLand) -> Question | None:
    query = """
        SELECT * FROM questions WHERE land IS NULL OR land = $1 ORDER BY RANDOM() LIMIT 1
    """

    question = await pool.fetchrow(query, land.value)

    if question is None:
        return None

    return Question.from_record(question)


async def get_general_questions(pool: Pool, limit: int = EXAM_GENERAL) -> list[Question]:
    query = """
        SELECT * FROM questions WHERE land IS NULL ORDER BY RANDOM() LIMIT $1
    """

    questions = await pool.fetch(query, limit)

    return [Question.from_record(question) for question in questions]


async def get_land_questions(
    pool: Pool, land: GermanLand, limit: int = EXAM_LAND
) -> list[Question]:
    query = """
        SELECT * FROM questions WHERE land = $1 ORDER BY RANDOM() LIMIT $2
    """

    questions = await pool.fetch(query, land.value, limit)

    return [Question.from_record(question) for question in questions]


async def create_exam_record(pool: Pool, telegram_id: int, correct_answers: int) -> None:
    query = """
        INSERT INTO exam_sessions (user_id, correct_answers)
        VALUES ($1, $2)
    """

    await pool.execute(query, telegram_id, correct_answers)


async def get_stats(pool: Pool, telegram_id: int) -> list[ExamSession]:
    query = """
        SELECT * FROM exam_sessions WHERE user_id = $1 ORDER BY created_at DESC
    """

    exam_sessions = await pool.fetch(query, telegram_id)

    return [ExamSession.from_record(session) for session in exam_sessions]
