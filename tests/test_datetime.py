from datetime import datetime

from assistant.tools.datetime import get_current_datetime


def test_get_current_datetime_returns_string():
    result = get_current_datetime()

    assert isinstance(result, str)


def test_get_current_datetime_has_expected_format():
    result = get_current_datetime()

    datetime_part = " ".join(result.split()[:2])

    parsed = datetime.strptime(datetime_part, "%Y-%m-%d %H:%M:%S")

    assert parsed is not None


def test_get_current_datetime_contains_date():
    result = get_current_datetime()

    date_part = result[:10]

    datetime.strptime(date_part, "%Y-%m-%d")
