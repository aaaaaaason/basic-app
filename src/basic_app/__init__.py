"""App configuration."""
import fastapi

from basic_app.lib import (
    config,
    exception,
    password,
    postgres,
)

from basic_app.routers import (
    user,
    google_signin,
)

from basic_app import (
    daos,
    services,
    routers,
)

class API(fastapi.FastAPI):
    """Wrap original FastAPI class for customization."""
    def __init__(self):
        super().__init__()

        exception.setup(self)

        self.include_router(google_signin.router)
        self.include_router(user.router)

def setup(conf: config.Config):
    """Initialize all dependencies here."""

    sessionmaker = postgres.create_sessionmaker(conf)
    #engine = postgres.create_engine(conf)

    password_hasher = password.Argon2PasswordHasher(conf)

    routers.GoogleSignin(
        conf.host,
        conf.google_client_id,
    )

    routers.User(
        services.User(
            sessionmaker=sessionmaker,
            hasher=password_hasher,
        )
    )

