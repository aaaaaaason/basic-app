"""Test user APIs."""
import dataclasses
import datetime as dt
import uuid
from typing import Type
import pytest
import httpx
from basic_app import (
    routers,
    services,
)
from tests import helper

def get_signup_request_body():
    return {
        'id':'40c0813a-6805-40e7-9f49-3ee69d6e0c98',
        'email':'user1@example.com',
        'username':'user1',
        'password':'password1',
    }

def get_signup_result():
    now = dt.datetime.now()
    return services.SignupResult(
        id='40c0813a-6805-40e7-9f49-3ee69d6e0c98',
        email='user1@example.com',
        username='user1',
        create_time=now,
        update_time=now,
    )

@dataclasses.dataclass
class StubUserService:
    signup_cmd:services.SignupCommand = None
    signup_result: services.SignupResult = None
    signup_raise: Type[Exception] = None

    async def signup(self, cmd: services.SignupCommand) -> services.SignupResult:
        self.signup_cmd = cmd
        if self.signup_raise:
            raise self.signup_raise
        return self.signup_result

@pytest.mark.medium
@pytest.mark.asyncio
async def test_signup_request():
    # Given I setup an user endpoint.
    signup_result = get_signup_result()
    stub_service = StubUserService(signup_result=signup_result)
    routers.User(stub_service)

    # When I send a signup request.
    body = get_signup_request_body()
    async with helper.get_http_client() as ac:
        resp: httpx.Response = await ac.post(
            url='/signup',
            json=body)

    # Then I should get expected SignupCommand
    cmd = stub_service.signup_cmd
    assert cmd, "signup service should be called."

    assert cmd.id == uuid.UUID(body['id']),\
        f"Got unexpect id \"{cmd.id}\" in signup command."
    assert cmd.email == body['email'],\
        f"Got unexpect email \"{cmd.email}\" in signup command."
    assert cmd.username == body['username'],\
        f"Got unexpect username \"{cmd.username}\" in signup command."
    assert cmd.password == body['password'],\
        f"Got unexpect password \"{cmd.password}\" in signup command."

    # And I should get expected SignupResponse
    out = resp.json()
    assert out['id'] == signup_result.id,\
        f"Got unexpect id \"{out['id']}\" in signup response."
    assert out['email'] == signup_result.email,\
        f"Got unexpect email \"{out['email']}\" in signup response."
    assert out['username'] == signup_result.username,\
        f"Got unexpect username \"{out['username']}\" in signup response."
    assert helper.parse_datetime(out['create_time']) == signup_result.create_time,\
        f"Got unexpect create_time \"{out['create_time']}\" in signup response."
    assert helper.parse_datetime(out['update_time']) == signup_result.update_time,\
        f"Got unexpect update_time \"{out['update_time']}\" in signup response."

def get_login_request_body():
    return {
        'email': 'user1@example.com',
        'password': 'password1'
    }

@pytest.mark.medium
@pytest.mark.asyncio
async def test_login_request():
    # Given I setup an user endpoint.
    login_result = get_login_result()
    stub_service = StubUserService(signup_result=signup_result)
    routers.User(stub_service)

    # When I send a signup request.
    body = get_signup_request_body()
    async with helper.get_http_client() as ac:
        resp: httpx.Response = await ac.post(
            url='/signup',
            json=body)

