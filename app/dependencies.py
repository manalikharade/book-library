"""FastAPI dependencies for services and DB."""
from fastapi import Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.services import BookService, BorrowingService, MemberService


def get_book_service(db: Session = Depends(get_db)) -> BookService:
    return BookService(db)


def get_member_service(db: Session = Depends(get_db)) -> MemberService:
    return MemberService(db)


def get_borrowing_service(db: Session = Depends(get_db)) -> BorrowingService:
    return BorrowingService(db)
