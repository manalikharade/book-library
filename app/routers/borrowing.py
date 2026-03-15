import logging

from fastapi import APIRouter, Depends, HTTPException

from .. import schemas
from ..dependencies import get_borrowing_service
from ..services import BorrowingService

logger = logging.getLogger(__name__)
router = APIRouter(tags=["borrowing"])

# Route order: specific paths before /{borrowing_id} to avoid 422


@router.post("/borrow", response_model=schemas.Borrowing)
def borrow_book(
    borrowing: schemas.BorrowingCreate,
    service: BorrowingService = Depends(get_borrowing_service),
):
    """Record when a member borrows a book"""
    db_borrowing = service.borrow_book(borrowing)
    if db_borrowing is None:
        raise HTTPException(
            status_code=400,
            detail="Cannot borrow: Book not found, not available, or member not found",
        )
    return db_borrowing


@router.post("/return", response_model=schemas.Borrowing)
def return_book(
    return_data: schemas.BorrowingReturn,
    service: BorrowingService = Depends(get_borrowing_service),
):
    """Record when a member returns a book"""
    db_borrowing = service.return_book(return_data.borrowing_id)
    if db_borrowing is None:
        raise HTTPException(
            status_code=404,
            detail="Borrowing record not found or book already returned",
        )
    return db_borrowing


@router.get("/active/all", response_model=list[schemas.Borrowing])
def list_active_borrowings(service: BorrowingService = Depends(get_borrowing_service)):
    """Get all currently active borrowings (books not yet returned)"""
    return service.list_active()


@router.get("/member/{member_id}/borrowed", response_model=list[schemas.Borrowing])
def get_member_current_books(
    member_id: int,
    service: BorrowingService = Depends(get_borrowing_service),
):
    """Get all books currently borrowed by a specific member"""
    member = service.member_repo.get(service.db, member_id)
    if member is None:
        raise HTTPException(status_code=404, detail="Member not found")
    return service.get_member_borrowed(member_id)


@router.get("/member/{member_id}/history", response_model=list[schemas.Borrowing])
def get_member_borrowing_history(
    member_id: int,
    service: BorrowingService = Depends(get_borrowing_service),
):
    """Get complete borrowing history for a member (borrowed and returned)"""
    if service.member_repo.get(service.db, member_id) is None:
        raise HTTPException(status_code=404, detail="Member not found")
    return service.get_member_history(member_id)


@router.get("/book/{book_id}/history", response_model=list[schemas.Borrowing])
def get_book_borrowing_history(
    book_id: int,
    service: BorrowingService = Depends(get_borrowing_service),
):
    """Get borrowing history for a specific book"""
    if service.book_repo.get(service.db, book_id) is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return service.get_book_history(book_id)


@router.get("/{borrowing_id}", response_model=schemas.Borrowing)
def get_borrowing(
    borrowing_id: int,
    service: BorrowingService = Depends(get_borrowing_service),
):
    """Get a specific borrowing record"""
    db_borrowing = service.get_borrowing(borrowing_id)
    if db_borrowing is None:
        raise HTTPException(status_code=404, detail="Borrowing record not found")
    return db_borrowing


@router.get("/", response_model=schemas.PaginatedResponse[schemas.Borrowing])
def list_borrowings(
    skip: int = 0,
    limit: int = 100,
    service: BorrowingService = Depends(get_borrowing_service),
):
    """List all borrowing records with pagination (returns items and total count)."""
    items, total = service.list_paginated(skip=skip, limit=limit)
    return schemas.PaginatedResponse(items=items, total=total)
