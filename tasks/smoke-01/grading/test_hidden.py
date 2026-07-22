"""Hidden suite for smoke-01 (public only because this is the smoke task)."""
import pytest

from timekit import parse_duration


def test_combined_units():
    assert parse_duration("1h30m") == 90


def test_combined_zero_padded_minutes():
    assert parse_duration("2h05m") == 125


def test_whitespace_tolerated():
    assert parse_duration(" 90m ") == 90


def test_regression_hours_only():
    assert parse_duration("2h") == 120


def test_regression_minutes_only():
    assert parse_duration("45m") == 45


def test_regression_invalid_raises():
    with pytest.raises(ValueError):
        parse_duration("later")
