"""Data access layer for books."""
import logging
from typing import List, Optional

from sqlalchemy.orm import Session

from app import models, schemas

logger = logging.getLogger(__name__)


class BookRepository:
    """Repository for book persistence."""

    @staticmethod
    def create(db: Session, book: schemas.BookCreate) -> models.Book:
        db_book = models.Book(title=book.title, author=book.author)
        db.add(db_book)
        db.commit()
        db.refresh(db_book)
        logger.debug("Created book id=%s", db_book.id)
        return db_book

    @staticmethod
    def get(db: Session, book_id: int) -> Optional[models.Book]:
        return db.query(models.Book).filter(models.Book.id == book_id).first()

    @staticmethod
    def get_all(db: Session, skip: int = 0, limit: int = 100) -> List[models.Book]:
        return db.query(models.Book).offset(skip).limit(limit).all()

    @staticmethod
    def count(db: Session) -> int:
        return db.query(models.Book).count()

    @staticmethod
    def get_available(db: Session) -> List[models.Book]:
        return db.query(models.Book).filter(models.Book.available.is_(True)).all()

    @staticmethod
    def update(db: Session, book_id: int, book_update: schemas.BookUpdate) -> Optional[models.Book]:
        db_book = db.query(models.Book).filter(models.Book.id == book_id).first()
        if not db_book:
            return None
        data = book_update.model_dump(exclude_unset=True)
        for key, value in data.items():
            setattr(db_book, key, value)
        db.add(db_book)
        db.commit()
        db.refresh(db_book)
        logger.debug("Updated book id=%s", book_id)
        return db_book

    @staticmethod
    def delete(db: Session, book_id: int) -> bool:
        db_book = db.query(models.Book).filter(models.Book.id == book_id).first()
        if not db_book:
            return False
        db.delete(db_book)
        db.commit()
        logger.debug("Deleted book id=%s", book_id)
        return True

    @staticmethod
    def set_available(db: Session, book_id: int, available: bool) -> None:
        db_book = db.query(models.Book).filter(models.Book.id == book_id).first()
        if db_book:
            db_book.available = available
            db.add(db_book)
            db.commit()
