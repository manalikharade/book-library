from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import schemas, crud
from ..database import get_db

router = APIRouter(tags=["borrowing"])

@router.post("/borrow", response_model=schemas.Borrowing)
def borrow_book(borrowing: schemas.BorrowingCreate, db: Session = Depends(get_db)):
    """Record when a member borrows a book"""
    db_borrowing = crud.borrow_book(db=db, borrowing=borrowing)
    if db_borrowing is None:
        raise HTTPException(
            status_code=400, 
            detail="Cannot borrow: Book not found, not available, or member not found"
        )
    return db_borrowing

@router.post("/return", response_model=schemas.Borrowing)
def return_book(return_data: schemas.BorrowingReturn, db: Session = Depends(get_db)):
    """Record when a member returns a book"""
    db_borrowing = crud.return_book(db=db, borrowing_id=return_data.borrowing_id)
    if db_borrowing is None:
        raise HTTPException(
            status_code=404, 
            detail="Borrowing record not found or book already returned"
        )
    return db_borrowing

# GET routes for specific paths (must come BEFORE the generic /{borrowing_id} route)
@router.get("/active/all", response_model=list[schemas.Borrowing])
def list_active_borrowings(db: Session = Depends(get_db)):
    """Get all currently active borrowings (books not yet returned)"""
    borrowings = crud.get_active_borrowings(db=db)
    return borrowings

@router.get("/member/{member_id}/borrowed", response_model=list[schemas.Borrowing])
def get_member_current_books(member_id: int, db: Session = Depends(get_db)):
    """Get all books currently borrowed by a specific member"""
    member = crud.get_member(db=db, member_id=member_id)
    if member is None:
        raise HTTPException(status_code=404, detail="Member not found")
    
    borrowings = crud.get_member_borrowed_books(db=db, member_id=member_id)
    return borrowings

@router.get("/member/{member_id}/history", response_model=list[schemas.Borrowing])
def get_member_borrowing_history(member_id: int, db: Session = Depends(get_db)):
    """Get complete borrowing history for a member (borrowed and returned)"""
    member = crud.get_member(db=db, member_id=member_id)
    if member is None:
        raise HTTPException(status_code=404, detail="Member not found")
    
    borrowings = crud.get_member_borrowing_history(db=db, member_id=member_id)
    return borrowings

@router.get("/book/{book_id}/history", response_model=list[schemas.Borrowing])
def get_book_borrowing_history(book_id: int, db: Session = Depends(get_db)):
    """Get borrowing history for a specific book"""
    book = crud.get_book(db=db, book_id=book_id)
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    
    borrowings = crud.get_book_borrowing_history(db=db, book_id=book_id)
    return borrowings

# Generic GET routes (must come AFTER specific routes)
@router.get("/{borrowing_id}", response_model=schemas.Borrowing)
def get_borrowing(borrowing_id: int, db: Session = Depends(get_db)):
    """Get a specific borrowing record"""
    db_borrowing = crud.get_borrowing(db=db, borrowing_id=borrowing_id)
    if db_borrowing is None:
        raise HTTPException(status_code=404, detail="Borrowing record not found")
    return db_borrowing

@router.get("/", response_model=list[schemas.Borrowing])
def list_borrowings(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """List all borrowing records with pagination"""
    borrowings = crud.get_all_borrowings(db=db, skip=skip, limit=limit)
    return borrowings
