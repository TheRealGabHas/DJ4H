import asyncio
import traceback

from config import LOGGER, RNGDLE_SYNC_INTERVAL
from utils.database.dao.rngdle import RNGdleDao
from utils.rngdle import RNGdle as RNGdleClient


async def _process_user(rng_client: RNGdleClient, db_user) -> None:
    """Fetch rolls for one user and store them into DB history."""
    try:
        # rng_client.get_user_rolls is synchronous (uses requests), run in thread
        rolls = rng_client.get_user_rolls(db_user.rng_username)
        if not rolls:
            LOGGER.debug(f"No rolls found for {db_user.rng_username}")
            return

        # rolls is a list of UserRolls objects, store each (upsert will ignore older ones)
        for roll in rolls:
            try:
                inserted = await RNGdleDao.upsert_rngdle(
                    user_id=db_user.user_id,
                    guild_id=db_user.guild_id,
                    date=roll.date,
                    score=roll.score,
                    number=roll.number,
                )
                if inserted:
                    LOGGER.info(
                        f"Stored/updated rngdle for {db_user.rng_username} (user {db_user.user_id}), score {roll.score} at {roll.date} number: {roll.number}"
                    )
            except Exception:
                LOGGER.error(
                    f"Failed upserting roll for {db_user.rng_username}: {traceback.format_exc()}"
                )
    except Exception:
        LOGGER.error(
            f"Failed fetching rolls for {db_user.rng_username}: {traceback.format_exc()}"
        )


async def rngdle_sync_loop():
    """Main loop: every hour fetch all registered users and sync their rolls."""
    rng_client = RNGdleClient()
    while True:
        try:
            LOGGER.info("RNGdle sync: starting pass to fetch registered users")
            users = await RNGdleDao.get_all_registered_users()
            if not users:
                LOGGER.info("RNGdle sync: no registered users found")
            else:
                for user in users:
                    await _process_user(rng_client, user)

            LOGGER.info(
                f"RNGdle sync: pass complete, sleeping {RNGDLE_SYNC_INTERVAL} seconds"
            )
        except Exception:
            LOGGER.error(f"RNGdle sync loop error: {traceback.format_exc()}")

        await asyncio.sleep(RNGDLE_SYNC_INTERVAL)


def schedule_rngdle_sync(bot) -> None:
    """Schedule the background sync loop on the bot event loop."""
    try:
        bot.loop.create_task(rngdle_sync_loop())
        LOGGER.info("RNGdle background sync scheduled")
    except Exception:
        LOGGER.error(
            f"Failed to schedule rngdle sync: {traceback.format_exc()}"
        )
