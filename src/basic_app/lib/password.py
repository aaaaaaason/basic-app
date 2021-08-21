"""Define password hasher."""
import argon2

from basic_app.lib import config

class PasswordHasher:
    """Define base password hasher."""

    def hash(self, password: str) -> str:
        """Hash the password."""
        raise NotImplementedError

    def verify(self, password: str, hash: str) -> bool:
        """Verify the password is matched."""
        raise NotImplementedError

    def check_rehash(self) -> bool:
        """Check if the user password needs rehash."""
        raise NotImplementedError

class Argon2PasswordHasher(PasswordHasher):
    """Password hasher using Argon2."""
    def __init__(self, conf: config.Config):
        # We can also refer to:
        # https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html#salting
        self._hasher = argon2.PasswordHasher(
            memory_cost=conf.argon2_memory_cost,
            time_cost=conf.argon2_time_cost,
            parallelism=conf.argon2_parallelism,
            hash_len=conf.argon2_hash_len,
            type=argon2.Type.ID,
        )

    def hash(self, password: str) -> str:
        return self._hasher.hash(password)

    def verify(self, password: str, hash: str) -> bool:
        return self._hasher.verify(hash, password)

    def check_rehash(self, hash: str) -> bool:
        return self._hasher.check_needs_rehash(hash)
