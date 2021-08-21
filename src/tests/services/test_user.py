"""Test user API."""
from typing import Type
import datetime as dt
import dataclasses
import pytest
from basic_app.lib import password
from basic_app import (
    services,
    daos,
    models,
)
from tests import helper

def get_signup_command() -> services.SignupCommand:
    return services.SignupCommand(
        id='40c0813a-6805-40e7-9f49-3ee69d6e0c98',
        email='user1@example.com',
        username='user1',
        password='password1',
    )

def get_dao_signup_result() -> daos.CreateUserResult:
    now = dt.datetime.now()
    return daos.CreateUserResult(
        conflict=False,
        user=models.User(
            id='40c0813a-6805-40e7-9f49-3ee69d6e0c98',
            email='user1@example.com',
            username='user1',
            create_time=now,
            update_time=now,
        ),
    )

@dataclasses.dataclass
class StubUserDao:
    signup_cmd:daos.CreateUserCommand = None
    signup_result: daos.CreateUserResult = None
    signup_raise: Type[Exception] = None

    async def create_user(self,
        cmd: daos.CreateUserCommand) -> daos.CreateUserResult:
        self.signup_cmd = cmd
        if self.signup_raise:
            raise self.signup_raise
        return self.signup_result

@dataclasses.dataclass
class StubPasswordHasher(password.PasswordHasher):
    hashed_password: str = 'this is a hashed password'
    verifiy_result: bool = False
    need_rehash_result: bool = False

    def hash(self, password):
        return self.hashed_password

    def verify(self, password: str, hash: str) -> bool:
        return self.verifiy_result

    def need_rehash_result(self, hash: str) -> bool:
        return self.need_rehash_result

@pytest.mark.asyncio
async def test_signup():
    # Given I prepare signup command and user service.
    service_cmd = get_signup_command()
    dao_signup_result = get_dao_signup_result()
    stub_dao = StubUserDao(signup_result=dao_signup_result)
    hasher = StubPasswordHasher()
    service = services.User(dao=stub_dao, hasher=hasher)

    # When I start doing signup
    out: services.SignupResult = await service.signup(service_cmd)

    # Then I should get expected dao SignupCommand.
    cmd = stub_dao.signup_cmd
    assert cmd, "signup dao should be called."

    assert cmd.id == service_cmd.id,\
        f"Got unexpect id \"{cmd.id}\" in signup command."
    assert cmd.email == service_cmd.email,\
        f"Got unexpect email \"{cmd.email}\" in signup command."
    assert cmd.username == service_cmd.username,\
        f"Got unexpect username \"{cmd.username}\" in signup command."
    assert cmd.password == hasher.hashed_password,\
        f"Password should be encrypted in signup command."

    # And I should get expected service SignupResult.
    expect = dao_signup_result.user
    assert out.id == expect.id,\
        f"Got unexpect id \"{out.id}\" in signup response."
    assert out.email == expect.email,\
        f"Got unexpect email \"{out['email']}\" in signup response."
    assert out.username == expect.username,\
        f"Got unexpect username \"{out['username']}\" in signup response."
    assert out.create_time == expect.create_time,\
        f"Got unexpect create_time \"{out.create_time}\" in signup response."
    assert out.update_time == expect.update_time,\
        f"Got unexpect update_time \"{out.update_time}\" in signup response."
