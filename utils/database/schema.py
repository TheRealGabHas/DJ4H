from sqlalchemy import BigInteger, Column, String

from .connection import Base


class Guild(Base):
    __tablename__ = "guilds"

    guild_id = Column(BigInteger, primary_key=True, nullable=False)
    channel_id = Column(BigInteger, primary_key=True, nullable=False)
    delay_second = Column(BigInteger, nullable=False)


class Message(Base):
    __tablename__ = "messages"

    message_id = Column(String(20), primary_key=True, nullable=False)
    guild_id = Column(BigInteger, nullable=False)
    author_id = Column(BigInteger, nullable=False)
    timestamp = Column(BigInteger, nullable=False)


class User(Base):
    __tablename__ = "users"

    user_id = Column(BigInteger, primary_key=True, nullable=False)
    guild_id = Column(BigInteger, nullable=False)
    score = Column(BigInteger, nullable=False)


class RNGdle(Base):
    __tablename__ = "rngdle"

    user_id = Column(BigInteger, primary_key=True, nullable=False)
    guild_id = Column(BigInteger, nullable=False)
    rng_username = Column(String(20), nullable=False)
    date = Column(BigInteger, nullable=False)
    score = Column(BigInteger, nullable=False)
    number = Column(BigInteger, nullable=False)


class RNGdleUser(Base):
    __tablename__ = "rngdleuser"

    user_id = Column(BigInteger, primary_key=True, nullable=False)
    guild_id = Column(BigInteger, nullable=False)
    rng_username = Column(String(20), nullable=False)
