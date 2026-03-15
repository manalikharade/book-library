"""Unit tests for fine calculation (no DB)."""
from datetime import date, datetime, timezone
from unittest.mock import MagicMock

import pytest

from app.services.borrowing_service import _calculate_fine


def _mock_borrowing(due_date: date):
    m = MagicMock()
    m.due_date = due_date
    return m


def test_fine_zero_when_returned_on_due_date():
    due = date(2025, 3, 10)
    ref = date(2025, 3, 10)
    borrowing = _mock_borrowing(due)
    assert _calculate_fine(borrowing, datetime.combine(ref, datetime.min.time().replace(tzinfo=timezone.utc))) == 0.0


def test_fine_zero_when_returned_before_due():
    due = date(2025, 3, 10)
    ref = date(2025, 3, 9)
    borrowing = _mock_borrowing(due)
    assert _calculate_fine(borrowing, datetime.combine(ref, datetime.min.time().replace(tzinfo=timezone.utc))) == 0.0


def test_fine_one_day_late():
    due = date(2025, 3, 10)
    ref = date(2025, 3, 11)
    borrowing = _mock_borrowing(due)
    # fine_per_day is 10 from settings
    got = _calculate_fine(borrowing, datetime.combine(ref, datetime.min.time().replace(tzinfo=timezone.utc)))
    assert got == 10.0


def test_fine_multiple_days_late():
    due = date(2025, 3, 10)
    ref = date(2025, 3, 15)
    borrowing = _mock_borrowing(due)
    got = _calculate_fine(borrowing, datetime.combine(ref, datetime.min.time().replace(tzinfo=timezone.utc)))
    assert got == 50.0  # 5 days * 10
