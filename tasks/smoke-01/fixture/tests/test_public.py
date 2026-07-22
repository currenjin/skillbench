import pytest

from timekit import parse_duration


def test_hours_only():
    assert parse_duration("2h") == 120


def test_minutes_only():
    assert parse_duration("45m") == 45


def test_invalid_raises():
    with pytest.raises(ValueError):
        parse_duration("soon")
