import datetime as dt
import dataclasses
from typing import Coroutine
from sqlalchemy import (
    select,
    or_,
)

from basic_app.lib import (
    exception,
    password,
    postgres,
)
from basic_app import models


@dataclasses.dataclass
class SignupCommand:
    id: str
    email: str
    username: str
    password: str

@dataclasses.dataclass
class SignupResult:
    id: str
    email: str
    username: str
    create_time: dt.datetime
    update_time: dt.datetime

@dataclasses.dataclass
class LoginCommand:
    email: str
    password: str

@dataclasses.dataclass
class LoginResult:
    id: str
    email: str
    username: str
    create_time: dt.datetime
    update_time: dt.datetime

class User:

    def __init__(self, sessionmaker: postgres.SessionMaker,
        hasher: password.PasswordHasher):
        self._sessionmaker = sessionmaker
        self._hasher = hasher

    async def signup(self,
        cmd: SignupCommand
        ) -> Coroutine[None, None, SignupResult]:

        hash_password = self._hasher.hash(cmd.password)
        now = dt.datetime.now()
        # TODO: send a verification mail? 2FA?

        async with self._sessionmaker(postgres.IsolationLevel.REPEATABLE_READ) as session:

            insert_result = await session.insert_on_conflict_do_nothing(models.User(
                id=cmd.id,
                email=cmd.email,
                username=cmd.username,
                password=hash_password,
                create_time=now,
                update_time=now,
            ))

            if insert_result.rowcount == 0:
                conflict_users = await session.select(
                    select(models.User).where(or_(
                        models.User.id == cmd.id,
                        models.User.email == cmd.email,
                        )))

                conflict_user = conflict_users[0]
                if cmd.email == conflict_user.email:
                    raise exception.AppException(
                        code=exception.ErrorCode.EMAIL_ALEADY_EXISTS,
                    )
                # User ID bumped from another email.
                elif cmd.user.id == conflict_user.id:
                    raise exception.AppException(
                        code=exception.ErrorCode.RESOURCE_ID_ALREADY_EXISTS,
                    )

        return SignupResult(
            id=cmd.id,
            email=cmd.email,
            username=cmd.username,
            create_time=now,
            update_time=now,
        )

    #async def login(self,
    #    cmd: LoginCommand
    #    ) -> Coroutine[None, None, LoginResult]:


