from typing import Sequence

from sqlalchemy.sql.expression import select

from utils.database import RNGdleUser, get_db


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
