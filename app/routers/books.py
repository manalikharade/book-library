import logging

from fastapi import APIRouter, Depends, HTTPException

from .. import schemas
from ..dependencies import get_book_service
from ..services import BookService

logger = logging.getLogger(__name__)
router = APIRouter(tags=["books"])

# Route order: literal paths before path params to avoid 422 (e.g. /available/all before /{book_id})


@router.get("/", response_model=schemas.PaginatedResponse[schemas.Book])
def list_books(
    skip: int = 0,
    limit: int = 100,
    service: BookService = Depends(get_book_service),
):
    """List all books with pagination (returns items and total count)."""
    items, total = service.list_paginated(skip=skip, limit=limit)
    return schemas.PaginatedResponse(items=items, total=total)


@router.post("/", response_model=schemas.Book)
def create_book(
    book: schemas.BookCreate,
    service: BookService = Depends(get_book_service),
):
    """Create a new book"""
    return service.create(book)


@router.get("/available/all", response_model=list[schemas.Book])
def list_available_books(service: BookService = Depends(get_book_service)):
    """List all available books (must be before GET /{book_id})."""
    return service.list_available()


@router.get("/{book_id}", response_model=schemas.Book)
def get_book(
    book_id: int,
    service: BookService = Depends(get_book_service),
):
    """Get a specific book by ID"""
    db_book = service.get(book_id)
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return db_book


@router.put("/{book_id}", response_model=schemas.Book)
def update_book(
    book_id: int,
    book_update: schemas.BookUpdate,
    service: BookService = Depends(get_book_service),
):
    """Update a book's details"""
    db_book = service.update(book_id, book_update)
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return db_book


@router.delete("/{book_id}")
def delete_book(
    book_id: int,
    service: BookService = Depends(get_book_service),
):
    """Delete a book"""
    deleted = service.delete(book_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Book not found")
    return {"message": "Book deleted successfully"}
