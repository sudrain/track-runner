from datetime import UTC, datetime

from app.routers.statistics import _month_range, _week_range


class TestWeekRange:
    def test_monday(self):
        monday = datetime(2026, 5, 18, 12, 0, 0, tzinfo=UTC)
        start, end = _week_range(monday)
        assert start.day == 18
        assert start.month == 5
        assert start.hour == 0
        assert end.day == 25
        assert end.month == 5

    def test_sunday(self):
        sunday = datetime(2026, 5, 24, 12, 0, 0, tzinfo=UTC)
        start, end = _week_range(sunday)
        assert start.day == 18
        assert end.day == 25


class TestMonthRange:
    def test_mid_month(self):
        dt = datetime(2026, 5, 15, 12, 0, 0, tzinfo=UTC)
        start, end = _month_range(dt)
        assert start.day == 1
        assert start.month == 5
        assert end.month == 6
        assert end.day == 1

    def test_december(self):
        dt = datetime(2026, 12, 15, 12, 0, 0, tzinfo=UTC)
        start, end = _month_range(dt)
        assert start.month == 12
        assert start.day == 1
        assert end.month == 1
        assert end.day == 1
        assert end.year == 2027

    def test_february_non_leap(self):
        dt = datetime(2027, 2, 15, 12, 0, 0, tzinfo=UTC)
        start, end = _month_range(dt)
        assert start.month == 2
        assert start.day == 1
        assert end.month == 3
        assert end.day == 1
