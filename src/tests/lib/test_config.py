"""Test file for basic_app.lib.config"""
import os
import pytest
from basic_app.lib import config

@pytest.mark.small
def test_must_read_env_exists():
    # Given I set an environment variable
    key, expect = "THIS_IS_FOR_TEST", "VALUE"
    os.environ[key] = expect

    # When I try to read env
    # pylint: disable=protected-access
    got = config._must_read_env(key)

    # Then I should get expected value
    assert got == expect, f"Expect to get \"{expect}\", but got \"{got}\""

    # Cleanup
    del os.environ[key]

@pytest.mark.small
def test_must_read_env_not_exists():
    # Given I set an environment variable
    key = "THIS_IS_FOR_TEST"
    if os.getenv(key):
        del os.environ[key]

    # When I try to read env
    # Then I should get an exception
    with pytest.raises(config.EnvironmentVariableNotFoundError):
        # pylint: disable=protected-access
        config._must_read_env(key)

@pytest.mark.small
def test_must_read_env_default_value():
    # When I try to read env
    # pylint: disable=protected-access
    key, default = "THIS_IS_FOR_TEST", "THIS_IS_DEFAULT_VALUE"
    got = config._must_read_env(key, default)

    # Then I should get default value
    assert got == default, f"Expect to get \"{default}\", but got \"{got}\""
