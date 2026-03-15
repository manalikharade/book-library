import logging
from datetime import datetime, timedelta, timezone

from sqlalchemy import and_
from sqlalchemy.orm import Session

from . import models, schemas
from .config import get_settings

logger = logging.getLogger(__name__)

# ============ BOOK CRUD OPERATIONS ============

def create_book(db: Session, book: schemas.BookCreate):
    db_book = models.Book(title=book.title, author=book.author)
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book

def get_book(db: Session, book_id: int):
    return db.query(models.Book).filter(models.Book.id == book_id).first()

def get_all_books(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Book).offset(skip).limit(limit).all()

def count_books(db: Session) -> int:
    return db.query(models.Book).count()

def get_available_books(db: Session):
    return db.query(models.Book).filter(models.Book.available == True).all()

def update_book(db: Session, book_id: int, book_update: schemas.BookUpdate):
    db_book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if db_book:
        update_data = book_update.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_book, key, value)
        db.commit()
        db.refresh(db_book)
    return db_book

def delete_book(db: Session, book_id: int):
    db_book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if db_book:
        db.delete(db_book)
        db.commit()
    return db_book

# ============ MEMBER CRUD OPERATIONS ============

def create_member(db: Session, member: schemas.MemberCreate):
    db_member = models.Member(
        name=member.name,
        contact_no=member.contact_no,
        address=member.address
    )
    db.add(db_member)
    db.commit()
    db.refresh(db_member)
    return db_member

def get_member(db: Session, member_id: int):
    return db.query(models.Member).filter(models.Member.id == member_id).first()

def get_all_members(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Member).offset(skip).limit(limit).all()

def count_members(db: Session) -> int:
    return db.query(models.Member).count()

def update_member(db: Session, member_id: int, member_update: schemas.MemberUpdate):
    db_member = db.query(models.Member).filter(models.Member.id == member_id).first()
    if db_member:
        update_data = member_update.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_member, key, value)
        db.commit()
        db.refresh(db_member)
    return db_member

def delete_member(db: Session, member_id: int):
    db_member = db.query(models.Member).filter(models.Member.id == member_id).first()
    if db_member:
        db.delete(db_member)
        db.commit()
    return db_member

# ============ BORROWING CRUD OPERATIONS ============

def borrow_book(db: Session, borrowing: schemas.BorrowingCreate):
    # Check if book exists and is available
    book = db.query(models.Book).filter(models.Book.id == borrowing.book_id).first()
    if not book or not book.available:
        return None
    
    # Check if member exists
    member = db.query(models.Member).filter(models.Member.id == borrowing.member_id).first()
    if not member:
        return None
    
    # Get settings for borrowing duration
    settings = get_settings()
    borrowed_date = datetime.now(tz=timezone.utc)
    due_date = borrowed_date + timedelta(days=settings.borrowing_duration_days)
    
    # Create borrowing record
    db_borrowing = models.Borrowing(
        book_id=borrowing.book_id,
        member_id=borrowing.member_id,
        borrowed_date=borrowed_date,
        due_date=due_date,
        is_active=True,
        fine=0.0
    )
    
    # Mark book as unavailable
    book.available = False
    
    db.add(db_borrowing)
    db.commit()
    db.refresh(db_borrowing)
    return db_borrowing

def return_book(db: Session, borrowing_id: int):
    borrowing = db.query(models.Borrowing).filter(models.Borrowing.id == borrowing_id).first()
    if not borrowing or not borrowing.is_active:
        return None

    settings = get_settings()
    returned_date = datetime.now(tz=timezone.utc)
    fine = calculate_fine(borrowing, returned_date)

    # Update borrowing record (explicit assign so ORM persists fine)
    borrowing.returned_date = returned_date
    borrowing.is_active = False
    borrowing.fine = float(fine)
    db.add(borrowing)

    book = db.query(models.Book).filter(models.Book.id == borrowing.book_id).first()
    if book:
        book.available = True
        db.add(book)

    db.commit()
    db.refresh(borrowing)
    return borrowing

def get_borrowing(db: Session, borrowing_id: int):
    return db.query(models.Borrowing).filter(models.Borrowing.id == borrowing_id).first()

def get_all_borrowings(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Borrowing).offset(skip).limit(limit).all()

def count_borrowings(db: Session) -> int:
    return db.query(models.Borrowing).count()

def calculate_fine(borrowing: models.Borrowing, ref_date: datetime):
    """Calculate fine for a borrowing based on return date and settings.
    Late days = calendar days after due date (no off-by-one).
    """
    settings = get_settings()
    due = borrowing.due_date.date() if hasattr(borrowing.due_date, 'date') else borrowing.due_date
    ref = ref_date.date() if hasattr(ref_date, 'date') else ref_date
    if ref <= due:
        return 0.0
    late_days = (ref - due).days
    fine = late_days * settings.fine_per_day
    return min(fine, settings.max_fine)

def get_active_borrowings(db: Session):
    """Get all currently active borrowings (not yet returned)"""
    borrowings = db.query(models.Borrowing).filter(models.Borrowing.is_active == True).all()
    
    # Calculate fine for each active borrowing based on current date
    
    current_date = datetime.now(tz=timezone.utc)
    
    for borrowing in borrowings:
        fine = calculate_fine(borrowing, current_date)
        borrowing.fine = fine
    
    return borrowings

def get_member_borrowed_books(db: Session, member_id: int):
    """Get all books currently borrowed by a specific member"""
    return db.query(models.Borrowing).filter(
        and_(
            models.Borrowing.member_id == member_id,
            models.Borrowing.is_active == True
        )
    ).all()

def get_member_borrowing_history(db: Session, member_id: int):
    """Get complete borrowing history for a member (borrowed and returned)"""
    return db.query(models.Borrowing).filter(
        models.Borrowing.member_id == member_id
    ).all()

def get_book_borrowing_history(db: Session, book_id: int):
    """Get borrowing history for a specific book"""
    return db.query(models.Borrowing).filter(
        models.Borrowing.book_id == book_id
    ).all()
