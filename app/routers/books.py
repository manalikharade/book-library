from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import schemas, crud
from ..database import get_db

router = APIRouter(tags=["books"])

@router.post("/", response_model=schemas.Book)
def create_book(book: schemas.BookCreate, db: Session = Depends(get_db)):
    """Create a new book"""
    return crud.create_book(db=db, book=book)

@router.get("/{book_id}", response_model=schemas.Book)
def get_book(book_id: int, db: Session = Depends(get_db)):
    """Get a specific book by ID"""
    db_book = crud.get_book(db=db, book_id=book_id)
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return db_book

@router.get("/", response_model=list[schemas.Book])
def list_books(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """List all books with pagination"""
    books = crud.get_all_books(db=db, skip=skip, limit=limit)
    return books

@router.get("/available/all", response_model=list[schemas.Book])
def list_available_books(db: Session = Depends(get_db)):
    """List all available books"""
    books = crud.get_available_books(db=db)
    return books

@router.put("/{book_id}", response_model=schemas.Book)
def update_book(book_id: int, book_update: schemas.BookUpdate, db: Session = Depends(get_db)):
    """Update a book's details"""
    db_book = crud.update_book(db=db, book_id=book_id, book_update=book_update)
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return db_book

@router.delete("/{book_id}")
def delete_book(book_id: int, db: Session = Depends(get_db)):
    """Delete a book"""
    db_book = crud.delete_book(db=db, book_id=book_id)
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return {"message": "Book deleted successfully"}
