"""Business logic for members."""
import logging
from typing import List, Optional

from sqlalchemy.orm import Session

from app import schemas
from app.repositories.member_repository import MemberRepository

logger = logging.getLogger(__name__)


class MemberService:
    """Service layer for member operations."""

    def __init__(self, db: Session):
        self.db = db
        self.repo = MemberRepository()

    def create(self, member: schemas.MemberCreate):
        return self.repo.create(self.db, member)

    def get(self, member_id: int):
        return self.repo.get(self.db, member_id)

    def list_paginated(self, skip: int = 0, limit: int = 100) -> tuple[List, int]:
        total = self.repo.count(self.db)
        items = self.repo.get_all(self.db, skip=skip, limit=limit)
        return items, total

    def update(self, member_id: int, member_update: schemas.MemberUpdate):
        return self.repo.update(self.db, member_id, member_update)

    def delete(self, member_id: int) -> bool:
        return self.repo.delete(self.db, member_id)
