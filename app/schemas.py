from datetime import datetime
from typing import List, Optional, TypeVar, Generic

from pydantic import BaseModel, ConfigDict, Field

T = TypeVar("T")


class PaginatedResponse(BaseModel, Generic[T]):
    """Generic paginated response with items and total count."""

    items: List[T]
    total: int


# Book Schemas
class BookBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=500)
    author: str = Field(..., min_length=1, max_length=300)


class BookCreate(BookBase):
    pass


class BookUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=500)
    author: Optional[str] = Field(None, min_length=1, max_length=300)


class Book(BookBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    available: bool
    created_at: datetime


# Member Schemas
class MemberBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    contact_no: str = Field(..., min_length=1, max_length=50)
    address: str = Field(..., min_length=1, max_length=500)


class MemberCreate(MemberBase):
    pass


class MemberUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    contact_no: Optional[str] = Field(None, min_length=1, max_length=50)
    address: Optional[str] = Field(None, min_length=1, max_length=500)


class Member(MemberBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime


# Borrowing Schemas
class BorrowingBase(BaseModel):
    book_id: int = Field(..., gt=0)
    member_id: int = Field(..., gt=0)


class BorrowingCreate(BorrowingBase):
    pass


class BorrowingReturn(BaseModel):
    borrowing_id: int = Field(..., gt=0)


class Borrowing(BorrowingBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    borrowed_date: datetime
    due_date: datetime
    returned_date: Optional[datetime]
    is_active: bool
    fine: float
    book: Book
    member: Member


class BorrowingSimple(BorrowingBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    borrowed_date: datetime
    due_date: datetime
    returned_date: Optional[datetime]
    is_active: bool
    fine: float
