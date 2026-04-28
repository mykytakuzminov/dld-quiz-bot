from dld_quiz_bot.db import repository as rp
from dld_quiz_bot.enums import GermanLand

TELEGRAM_ID = 123456789
USERNAME = "test_user"
SELECTED_LAND = GermanLand("Bayern")
NEW_LAND = GermanLand("Berlin")
CORRECT_ANSWERS = 20


async def test_create_user(pool):
    await rp.create_user(pool, TELEGRAM_ID, USERNAME, SELECTED_LAND)


async def test_get_user(pool):
    await rp.create_user(pool, TELEGRAM_ID, USERNAME, SELECTED_LAND)
    user = await rp.get_user(pool, TELEGRAM_ID)
    assert user is not None
    assert user.telegram_id == TELEGRAM_ID
    assert user.username == USERNAME
    assert user.selected_land == SELECTED_LAND


async def test_get_user_not_found(pool):
    user = await rp.get_user(pool, 999999999)
    assert user is None


async def test_change_user_land(pool):
    await rp.create_user(pool, TELEGRAM_ID, USERNAME, SELECTED_LAND)
    await rp.change_user_land(pool, TELEGRAM_ID, NEW_LAND)
    user = await rp.get_user(pool, TELEGRAM_ID)
    assert user.selected_land == NEW_LAND


async def test_get_random_question(pool, add_general_question):
    await rp.create_user(pool, TELEGRAM_ID, USERNAME, SELECTED_LAND)
    question = await rp.get_random_question(pool, TELEGRAM_ID)
    assert question is not None
    assert isinstance(question.id, int)
    assert isinstance(question.text, str)
    assert isinstance(question.options, list)
    assert len(question.options) == 4
    assert isinstance(question.correct_answer, str)


async def test_get_random_questions_return_none(pool):
    question = await rp.get_random_question(pool, TELEGRAM_ID)
    assert question is None
    await rp.create_user(pool, TELEGRAM_ID, USERNAME, SELECTED_LAND)
    question = await rp.get_random_question(pool, TELEGRAM_ID)
    assert question is None


async def test_get_general_questions(pool, add_general_question):
    questions = await rp.get_general_questions(pool, limit=1)
    assert len(questions) == 1

    question = questions[0]
    assert isinstance(question.id, int)
    assert isinstance(question.text, str)
    assert isinstance(question.options, list)
    assert len(question.options) == 4
    assert isinstance(question.correct_answer, str)


async def test_get_general_questions_return_empty_list(pool):
    questions = await rp.get_general_questions(pool, limit=1)
    assert len(questions) == 0


async def test_get_land_questions(pool, add_land_question):
    await rp.create_user(pool, TELEGRAM_ID, USERNAME, SELECTED_LAND)
    questions = await rp.get_land_questions(pool, TELEGRAM_ID, limit=1)
    assert len(questions) == 1

    question = questions[0]
    assert isinstance(question.id, int)
    assert isinstance(question.text, str)
    assert isinstance(question.options, list)
    assert len(question.options) == 4
    assert isinstance(question.correct_answer, str)


async def test_get_land_questions_return_empty_list(pool):
    questions = await rp.get_land_questions(pool, TELEGRAM_ID, limit=1)
    assert len(questions) == 0


async def test_create_exam_record(pool):
    await rp.create_user(pool, TELEGRAM_ID, USERNAME, SELECTED_LAND)
    await rp.create_exam_record(pool, TELEGRAM_ID, CORRECT_ANSWERS)
