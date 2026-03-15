"""Data access layer for borrowings."""
import logging
from datetime import datetime
from typing import List, Optional

from sqlalchemy import and_
from sqlalchemy.orm import Session

from app import models

logger = logging.getLogger(__name__)


class BorrowingRepository:
    """Repository for borrowing persistence."""

    @staticmethod
    def create(
        db: Session,
        book_id: int,
        member_id: int,
        borrowed_date: datetime,
        due_date: datetime,
        is_active: bool = True,
        fine: float = 0.0,
    ) -> models.Borrowing:
        db_borrowing = models.Borrowing(
            book_id=book_id,
            member_id=member_id,
            borrowed_date=borrowed_date,
            due_date=due_date,
            is_active=is_active,
            fine=fine,
        )
        db.add(db_borrowing)
        db.commit()
        db.refresh(db_borrowing)
        logger.debug("Created borrowing id=%s", db_borrowing.id)
        return db_borrowing

    @staticmethod
    def get(db: Session, borrowing_id: int) -> Optional[models.Borrowing]:
        return db.query(models.Borrowing).filter(models.Borrowing.id == borrowing_id).first()

    @staticmethod
    def get_all(db: Session, skip: int = 0, limit: int = 100) -> List[models.Borrowing]:
        return db.query(models.Borrowing).offset(skip).limit(limit).all()

    @staticmethod
    def count(db: Session) -> int:
        return db.query(models.Borrowing).count()

    @staticmethod
    def get_active(db: Session) -> List[models.Borrowing]:
        return db.query(models.Borrowing).filter(models.Borrowing.is_active.is_(True)).all()

    @staticmethod
    def update_return(
        db: Session,
        borrowing_id: int,
        returned_date: datetime,
        is_active: bool,
        fine: float,
    ) -> Optional[models.Borrowing]:
        borrowing = db.query(models.Borrowing).filter(models.Borrowing.id == borrowing_id).first()
        if not borrowing:
            return None
        borrowing.returned_date = returned_date
        borrowing.is_active = is_active
        borrowing.fine = float(fine)
        db.add(borrowing)
        db.commit()
        db.refresh(borrowing)
        logger.debug("Updated borrowing return id=%s fine=%s", borrowing_id, fine)
        return borrowing

    @staticmethod
    def get_member_borrowed(db: Session, member_id: int) -> List[models.Borrowing]:
        return (
            db.query(models.Borrowing)
            .filter(
                and_(
                    models.Borrowing.member_id == member_id,
                    models.Borrowing.is_active.is_(True),
                )
            )
            .all()
        )

    @staticmethod
    def get_member_history(db: Session, member_id: int) -> List[models.Borrowing]:
        return db.query(models.Borrowing).filter(models.Borrowing.member_id == member_id).all()

    @staticmethod
    def get_book_history(db: Session, book_id: int) -> List[models.Borrowing]:
        return db.query(models.Borrowing).filter(models.Borrowing.book_id == book_id).all()
