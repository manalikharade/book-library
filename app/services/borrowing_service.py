"""Business logic for borrowings and fine calculation."""
import logging
from datetime import datetime, timedelta, timezone
from typing import List, Optional

from sqlalchemy.orm import Session

from app import models, schemas
from app.config import get_settings
from app.repositories.book_repository import BookRepository
from app.repositories.borrowing_repository import BorrowingRepository
from app.repositories.member_repository import MemberRepository

logger = logging.getLogger(__name__)


def _calculate_fine(borrowing: models.Borrowing, ref_date: datetime) -> float:
    """Compute late fine: calendar days after due date × fine_per_day, capped at max_fine."""
    settings = get_settings()
    due = borrowing.due_date.date() if hasattr(borrowing.due_date, "date") else borrowing.due_date
    ref = ref_date.date() if hasattr(ref_date, "date") else ref_date
    if ref <= due:
        return 0.0
    late_days = (ref - due).days
    fine = late_days * settings.fine_per_day
    return min(fine, settings.max_fine)


class BorrowingService:
    """Service layer for borrowing and return operations."""

    def __init__(self, db: Session):
        self.db = db
        self.borrowing_repo = BorrowingRepository()
        self.book_repo = BookRepository()
        self.member_repo = MemberRepository()

    def borrow_book(self, data: schemas.BorrowingCreate) -> Optional[models.Borrowing]:
        book = self.book_repo.get(self.db, data.book_id)
        if not book or not book.available:
            logger.warning("Borrow rejected: book_id=%s not found or not available", data.book_id)
            return None
        member = self.member_repo.get(self.db, data.member_id)
        if not member:
            logger.warning("Borrow rejected: member_id=%s not found", data.member_id)
            return None
        settings = get_settings()
        borrowed_date = datetime.now(tz=timezone.utc)
        due_date = borrowed_date + timedelta(days=settings.borrowing_duration_days)
        borrowing = self.borrowing_repo.create(
            self.db,
            book_id=data.book_id,
            member_id=data.member_id,
            borrowed_date=borrowed_date,
            due_date=due_date,
            is_active=True,
            fine=0.0,
        )
        self.book_repo.set_available(self.db, data.book_id, False)
        logger.info("Book borrowed: borrowing_id=%s book_id=%s member_id=%s", borrowing.id, data.book_id, data.member_id)
        return borrowing

    def return_book(self, borrowing_id: int) -> Optional[models.Borrowing]:
        borrowing = self.borrowing_repo.get(self.db, borrowing_id)
        if not borrowing or not borrowing.is_active:
            logger.warning("Return rejected: borrowing_id=%s not found or already returned", borrowing_id)
            return None
        returned_date = datetime.now(tz=timezone.utc)
        fine = _calculate_fine(borrowing, returned_date)
        updated = self.borrowing_repo.update_return(
            self.db, borrowing_id, returned_date, is_active=False, fine=fine
        )
        if updated:
            self.book_repo.set_available(self.db, borrowing.book_id, True)
            logger.info("Book returned: borrowing_id=%s fine=%s", borrowing_id, fine)
        return updated

    def get_borrowing(self, borrowing_id: int):
        return self.borrowing_repo.get(self.db, borrowing_id)

    def list_paginated(self, skip: int = 0, limit: int = 100) -> tuple[List, int]:
        total = self.borrowing_repo.count(self.db)
        items = self.borrowing_repo.get_all(self.db, skip=skip, limit=limit)
        return items, total

    def list_active(self) -> List[models.Borrowing]:
        """Active borrowings with fine computed for display (not persisted)."""
        borrowings = self.borrowing_repo.get_active(self.db)
        now = datetime.now(tz=timezone.utc)
        for b in borrowings:
            b.fine = _calculate_fine(b, now)
        return borrowings

    def get_member_borrowed(self, member_id: int) -> List[models.Borrowing]:
        return self.borrowing_repo.get_member_borrowed(self.db, member_id)

    def get_member_history(self, member_id: int) -> List[models.Borrowing]:
        return self.borrowing_repo.get_member_history(self.db, member_id)

    def get_book_history(self, book_id: int) -> List[models.Borrowing]:
        return self.borrowing_repo.get_book_history(self.db, book_id)
