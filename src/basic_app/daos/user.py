"""Define user dao."""
import datetime as dt
import dataclasses
from sqlalchemy import orm, engine, select, or_
from sqlalchemy.ext import asyncio
from sqlalchemy.dialects import postgresql
from sqlalchemy.engine import cursor
from basic_app import models

@dataclasses.dataclass
class CreateUserCommand:
    id: str
    email: str
    username: str
    password: str
    create_time: dt.datetime
    update_time: dt.datetime

@dataclasses.dataclass
class CreateUserResult:
    conflict: bool
    user: models.User

class User:
    """Data access object for user model."""
    def __init__(self, sessionmaker: orm.sessionmaker):
        self._sessionmaker = sessionmaker

    async def create(self, cmd: CreateUserCommand) -> CreateUserResult:
        session: orm.Session = self._sessionmaker()

        # We can do the same thing below by using one bigger raw query.
        async with session.begin():
            await session.execute("SET TRANSACTION ISOLATION LEVEL REPEATABLE READ")

            insert_stmt = postgresql.insert(models.User).values(
                id=cmd.id,
                email=cmd.email,
                username=cmd.username,
                password=cmd.password,
                create_time=cmd.create_time,
                update_time=cmd.update_time,
            )
            do_nothing_stmt = insert_stmt.on_conflict_do_nothing()

            insert_result: cursor.CursorResult = await session.execute(do_nothing_stmt)

            select_result = await session.execute(
                select(models.User).
                    where(or_(
                        models.User.id == cmd.id,
                        models.User.email == cmd.email,
                        )),
            )

            user = select_result.fetchone()['User']

        return CreateUserResult(
            conflict=insert_result.rowcount == 0,
            user=models.User(
                id=user.id,
                email=user.email,
                username=user.username,
                create_time=user.create_time,
                update_time=user.update_time,
            ),
        )




