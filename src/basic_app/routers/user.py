"""User API handlers."""
import uuid
import datetime as dt
import fastapi
import pydantic

from basic_app import services

router = fastapi.APIRouter()

_controller = None

class SignupRequestBody(pydantic.BaseModel):
    id: uuid.UUID
    email: pydantic.EmailStr
    username: pydantic.constr(min_length=1, max_length=64)
    password: pydantic.constr(min_length=1, max_length=256)

class SignupResult(pydantic.BaseModel):
    id: uuid.UUID
    email: pydantic.EmailStr
    username: pydantic.constr(min_length=1, max_length=64)
    create_time: dt.datetime
    update_time: dt.datetime

@router.post("/signup", response_model=SignupResult)
async def signup(body: SignupRequestBody):
    return await _controller.signup(body)

class LoginRequestBody(pydantic.BaseModel):
    email: pydantic.EmailStr
    password: pydantic.constr(min_length=1, max_length=256)

class LoginResult(pydantic.BaseModel):
    id: uuid.UUID
    email: pydantic.EmailStr
    username: pydantic.constr(min_length=1, max_length=64)
    create_time: dt.datetime
    update_time: dt.datetime

@router.post("/login", response_model=LoginResult)
async def login(body: LoginRequestBody):
    return await _controller.login(body)

class User:
    """Define router."""

    def __init__(self, service: services.User):
        self._service = service
        global _controller
        _controller = self

    async def signup(self, body: SignupRequestBody):
        """The entrypoint of POST /signup request."""
        result = await self._service.signup(services.SignupCommand(
            id=body.id,
            email=body.email,
            username=body.username,
            password=body.password
        ))
        return SignupResult(
            id=result.id,
            email=result.email,
            username=result.username,
            create_time=result.create_time,
            update_time=result.update_time
        )

    async def login(self, body: LoginRequestBody):
        """The entrypoint of POST /login request."""
        result = await self._service.login(services.LoginCommand(
            email=body.email,
            password=body.password
        ))
        return LoginResult(
            id=result.id,
            email=result.email,
            username=result.username,
            create_time=result.create_time,
            update_time=result.update_time
        )
