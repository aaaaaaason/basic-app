"""Provide logging utility"""
import logging
from basic_app.lib import config

def _get_logging_level(level: str) -> int:
    """Returns logging level for Python logging module from str.

    Args:
      level: a string which is expected to get from environment variables.
    Returns:
      Corrsponding logging level defined in Python logging module.
    """
    mapping = {
        "FATAL": logging.FATAL,
        "DEBUG": logging.DEBUG,
        "WARNING": logging.WARNING,
        "INFO": logging.INFO,
        "ERROR": logging.ERROR,
    }
    return mapping.get(level, logging.INFO)

def setup(conf: config.Config):
    """Setup default logger

    Args:
      level: Logging level, which may be read from environment variables.
      fmt: Message format for logging.
    """

    logging.basicConfig(
        format=conf.logging_fmt,
        level=_get_logging_level(conf.logging_level),
        force=True
    )
