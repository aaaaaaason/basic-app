"""Configuration store is here"""
import os
import logging
import dotenv

_config = None

class EnvironmentVariableNotFoundError(Exception):
    pass

def _must_read_env(name: str, default: str = None) -> str:
    """Read environment variable.

    The program raises EnvironmentVariableNotFoundError if
    target name does not exists, and default value is not specified.

    Args:
      name: The name of the environment variable.
      default: Default value when no such variable.
    Returns:
      The value of the environment varible.
    Raises:
      EnvironmentVariableNotFoundError: If
    """
    value = os.getenv(name, default)
    if not value:
        logging.fatal("Cannot read variable \"%s\" "
            "and no default value specifed.", name)
        raise EnvironmentVariableNotFoundError("No")
    return value

class Config:
    """Stores configuration for properly initialize other module."""

    def __init__(self, envfile: str):
        """Initialize config object.

        Args:
          envfile: Filepath to read dotenv.
        """
        logging.info("Initializing config object.")
        if os.path.exists(envfile):
            logging.info("Loading dotenv from path \"%s\"", envfile)
            dotenv.load_dotenv(envfile)

        # Postgres
        self.postgres_user = _must_read_env("POSTGRES_USER")
        self.postgres_passwd = _must_read_env("POSTGRES_PASSWD")
        self.postgres_host = _must_read_env("POSTGRES_HOST")
        self.postgres_port = _must_read_env("POSTGRES_PORT")
        self.postgres_db = _must_read_env("POSTGRES_DB")

        # Argon2
        self.argon2_memory_cost = _must_read_env("ARGON2_MEMORY_COST", 16384)
        self.argon2_time_cost = _must_read_env("ARGON2_TIME_COST", 2)
        self.argon2_parallelism = _must_read_env("ARGON2_PARALLELISM", 1)
        self.argon2_hash_len = _must_read_env("ARGON2_HASH_LEN", 32)

        # App
        self.host = _must_read_env("APP_HOST")
        self.port = _must_read_env("APP_PORT")
        self.logging_level = _must_read_env("APP_LOGGING_LEVEL", "INFO")
        self.logging_fmt = _must_read_env("APP_LOGGING_FMT", "%(asctime)s %(levelname)s %(module)s %(lineno)d %(message)s")
        self.google_client_id = _must_read_env("APP_GOOGLE_CLIENT_ID")

def setup(envfile: str = ".env") -> Config:
    """Returns a singleton Config object

    Args:
      envfile: Filepath to read dotenv.
    Returns:
      Config object for quering configuration.
    """
    global _config
    if not _config:
        _config = Config(envfile)
    return _config
