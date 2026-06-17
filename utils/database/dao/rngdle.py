from typing import Sequence

from sqlalchemy.sql.expression import select

from utils.database import RNGdle, RNGdleUser, get_db


class RNGdleDao:
    @staticmethod
    async def register_user(user_id: int, guild_id: int, username: str) -> None:
        async for session in get_db():
            rngdle_user = RNGdleUser(
                user_id=user_id, guild_id=guild_id, rng_username=username
            )
            session.add(rngdle_user)
            await session.commit()

    @staticmethod
    async def get_registered_users(
        guild_id: int,
    ) -> Sequence[RNGdleUser] | None:
        async for session in get_db():
            users = await session.execute(
                select(RNGdleUser).filter(RNGdleUser.guild_id == guild_id)
            )
            return users.scalars().all()
        return None

    @staticmethod
    async def get_all_registered_users() -> Sequence[RNGdleUser] | None:
        """Return all registered RNGdle users across guilds."""
        async for session in get_db():
            users = await session.execute(select(RNGdleUser))
            return users.scalars().all()
        return None

    @staticmethod
    async def upsert_rngdle(
        user_id: int,
        guild_id: int,
        date: int,
        score: int,
        number: int,
    ) -> bool:
        """
        INSERT a roll into RNGdle history if it does not already exist.
        Returns True if inserted, False if an identical roll already exists.
        We consider a roll identical if user_id + date + number match an existing row.
        """
        async for session in get_db():
            existing = await session.execute(
                select(RNGdle).filter(
                    RNGdle.user_id == user_id,
                    RNGdle.date == date,
                    RNGdle.number == number,
                )
            )
            existing_row = existing.scalars().first()
            if existing_row is not None:
                return False

            rng = RNGdle(
                user_id=user_id,
                guild_id=guild_id,
                date=date,
                score=score,
                number=number,
            )
            session.add(rng)
            await session.commit()
            return True
