"""Data access layer for members."""
import logging
from typing import List, Optional

from sqlalchemy.orm import Session

from app import models, schemas

logger = logging.getLogger(__name__)


class MemberRepository:
    """Repository for member persistence."""

    @staticmethod
    def create(db: Session, member: schemas.MemberCreate) -> models.Member:
        db_member = models.Member(
            name=member.name,
            contact_no=member.contact_no,
            address=member.address,
        )
        db.add(db_member)
        db.commit()
        db.refresh(db_member)
        logger.debug("Created member id=%s", db_member.id)
        return db_member

    @staticmethod
    def get(db: Session, member_id: int) -> Optional[models.Member]:
        return db.query(models.Member).filter(models.Member.id == member_id).first()

    @staticmethod
    def get_all(db: Session, skip: int = 0, limit: int = 100) -> List[models.Member]:
        return db.query(models.Member).offset(skip).limit(limit).all()

    @staticmethod
    def count(db: Session) -> int:
        return db.query(models.Member).count()

    @staticmethod
    def update(
        db: Session, member_id: int, member_update: schemas.MemberUpdate
    ) -> Optional[models.Member]:
        db_member = db.query(models.Member).filter(models.Member.id == member_id).first()
        if not db_member:
            return None
        data = member_update.model_dump(exclude_unset=True)
        for key, value in data.items():
            setattr(db_member, key, value)
        db.add(db_member)
        db.commit()
        db.refresh(db_member)
        logger.debug("Updated member id=%s", member_id)
        return db_member

    @staticmethod
    def delete(db: Session, member_id: int) -> bool:
        db_member = db.query(models.Member).filter(models.Member.id == member_id).first()
        if not db_member:
            return False
        db.delete(db_member)
        db.commit()
        logger.debug("Deleted member id=%s", member_id)
        return True
