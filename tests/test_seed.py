from pathlib import Path

from dld_quiz_bot.db.seed import load_questions_from_json, seed
from dld_quiz_bot.paths import find_project_root

TOTAL_QUESTIONS = 460
QUERY = "SELECT COUNT(*) FROM questions"
ROOT = find_project_root()
CORRECT_PATH = ROOT / "data" / "questions.json"
INVALID_PATH = Path("/nonexistent/deep/folder/file.py")


def test_load_questions_from_json():
    questions = load_questions_from_json(CORRECT_PATH)
    assert len(questions) == TOTAL_QUESTIONS


async def test_seed(pool):
    await seed(pool, CORRECT_PATH)
    assert await pool.fetchval(QUERY) == TOTAL_QUESTIONS


async def test_seed_data_not_found(pool):
    await seed(pool, INVALID_PATH)
    assert await pool.fetchval(QUERY) == 0
