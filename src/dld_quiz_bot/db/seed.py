import asyncio
import json
from os import getenv
from pathlib import Path
from typing import Any

from asyncpg import Pool
from dotenv import load_dotenv

from dld_quiz_bot.db.database import close_pool, create_pool
from dld_quiz_bot.paths import find_project_root


def load_questions_from_json(filepath: Path) -> Any:
    with open(filepath, encoding="utf-8") as f:
        questions = json.load(f)
    return questions


async def seed(pool: Pool) -> None:
    try:
        root = find_project_root()
        path = root / "data" / "questions.json"

        if path.exists():
            await pool.execute("TRUNCATE questions RESTART IDENTITY")
            questions = load_questions_from_json(path)

            for question in questions:
                query = """
                    INSERT INTO questions (text, options, correct_answer, topic, land)
                    VALUES ($1, $2, $3, $4, $5)
                """

                text = question["text"]
                options = json.dumps(question["options"], ensure_ascii=False)
                correct_answer = question["correct_answer"]
                topic = question["topic"]
                land = question["land"]

                await pool.execute(query, text, options, correct_answer, topic, land)
        else:
            print(f"Seed data not found at {path}, skipping insert.")
    except Exception as e:
        print(f"Could not seed data: {e}")


load_dotenv()

POOL = getenv("ASYNCPG_URL")


async def main() -> None:
    if POOL is None:
        raise ValueError("ASYNCPG_URL is not set")

    pool = await create_pool(POOL)
    await seed(pool)
    await close_pool(pool)


if __name__ == "__main__":
    asyncio.run(main())
