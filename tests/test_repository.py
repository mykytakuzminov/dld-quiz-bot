from dld_quiz_bot.db import repository as rp
from dld_quiz_bot.enums import GermanLand

TELEGRAM_ID = 123456789
USERNAME = "test_user"
SELECTED_LAND = GermanLand("Bayern")
NEW_LAND = GermanLand("Berlin")


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
