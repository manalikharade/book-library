"""Business logic for books."""
import logging
from typing import List, Optional

from sqlalchemy.orm import Session

from app import schemas
from app.repositories.book_repository import BookRepository

logger = logging.getLogger(__name__)


class BookService:
    """Service layer for book operations."""

    def __init__(self, db: Session):
        self.db = db
        self.repo = BookRepository()

    def create(self, book: schemas.BookCreate):
        return self.repo.create(self.db, book)

    def get(self, book_id: int) -> Optional[schemas.Book]:
        return self.repo.get(self.db, book_id)

    def list_paginated(self, skip: int = 0, limit: int = 100) -> tuple[List, int]:
        total = self.repo.count(self.db)
        items = self.repo.get_all(self.db, skip=skip, limit=limit)
        return items, total

    def list_available(self):
        return self.repo.get_available(self.db)

    def update(self, book_id: int, book_update: schemas.BookUpdate):
        return self.repo.update(self.db, book_id, book_update)

    def delete(self, book_id: int) -> bool:
        return self.repo.delete(self.db, book_id)
