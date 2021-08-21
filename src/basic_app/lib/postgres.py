"""Provide SQLAlchemy engine for postgres"""
from __future__ import annotations
from typing import (
    List,
    Any,
)
import logging
from enum import Enum
import sqlalchemy as sa
from sqlalchemy import orm
from sqlalchemy.ext import asyncio
from sqlalchemy.dialects import postgresql as pg

from basic_app.lib import config
from basic_app.models import base

class IsolationLevel(Enum):
    """Define transaction isolation level."""
    READ_COMMITTED = "READ COMMITED"
    REPEATABLE_READ = "REPEATABLE READ"

class Session:
    """Create own session."""
    def __init__(self, session: orm.Session,
        isolation_level: IsolationLevel = None):
        self._session = session
        self._isolation_level = isolation_level

    async def __aenter__(self) -> Session:
        """Enter transaction."""
        await self._session.begin()
        if self._isolation_level:
            await self._session.execute(
                "SET TRANSACTION ISOLATION LEVEL {}".format(
                    self._isolation_level.value,
                )
            )
        return self

    async def __aexit__(self, exc_type, exc, tb):
        """
        Commit transaction if no exception occured, otherwise
        we do a rollback.
        """
        if exc_type:
            await self._session.rollback()
        else:
            await self._session.commit()

    async def insert(self, value: base.Base):
        """Insert one record.

        Args:
          values: A SQLAlchemy model instance.
        """
        stmt = sa.insert(type(value)).values(**value.to_dict())
        return await self._session.execute(stmt)

    async def insert_on_conflict_do_nothing(self,
        value: base.Base, conflict_columns: List[str] = None):
        """Insert one record, do nothing for conflict.

        Args:
          values: A SQLAlchemy model instance.
          conflict_columns: Which columns to check for conflict.
        """
        stmt = pg.insert(type(value)).values(**value.to_dict())
        stmt = stmt.on_conflict_do_nothing(
            index_elements=conflict_columns,
        )
        return await self._session.execute(stmt)

    async def select(self, stmt: Any) -> List[base.Base]:
        """Do a SQL SELECT.

        Args:
          stmt: The statement of SELECT represented in SQLAlchemy.
        Returns:
          List of SQLAlchemy objects.
        """
        result = await self._session.execute(stmt)
        return result.scalars().all()

class SessionMaker:
    """Create own sessionmaker."""
    def __init__(self, sessionmaker: orm.sessionmaker):
        self._sessionmaker = sessionmaker

    def __call__(self, isolation_level: IsolationLevel = None) -> Session:
        return Session(self._sessionmaker(), isolation_level)


def create_sessionmaker(conf: config.Config) -> SessionMaker:
    """Create async SQLAlchemy database engine"""

    url = "postgresql+asyncpg://{name}:{passwd}@{host}:{port}/{db}".format(
        name=conf.postgres_user,
        passwd=conf.postgres_passwd,
        host=conf.postgres_host,
        port=conf.postgres_port,
        db=conf.postgres_db,
    )

    engine = asyncio.create_async_engine(url, echo=False)
    logging.info("Postgres engine created.")
    return SessionMaker(
        orm.sessionmaker(
            bind=engine,
            expire_on_commit=False,
            class_=asyncio.AsyncSession)
        )
