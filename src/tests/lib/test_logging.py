"""Test file for basic_app.lib.logging"""
import logging
import basic_app.lib.logging as lg

def test_get_logging_level():
    # When
    # pylint: disable=protected-access
    level = lg._get_logging_level("DEBUG")

    # Then
    assert level == logging.DEBUG, f"Got unexpected log level \"{level}\""

def test_get_logging_level_default_level():
    # When
    # pylint: disable=protected-access
    level = lg._get_logging_level("")

    # Then
    assert level == logging.INFO, f"Got unexpected log level \"{level}\""
