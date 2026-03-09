from pydantic import BaseModel
from datetime import datetime
from typing import Optional

# Book Schemas
class BookBase(BaseModel):
    title: str
    author: str

class BookCreate(BookBase):
    pass

class BookUpdate(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None

class Book(BookBase):
    id: int
    available: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

# Member Schemas
class MemberBase(BaseModel):
    name: str
    contact_no: str
    address: str

class MemberCreate(MemberBase):
    pass

class MemberUpdate(BaseModel):
    name: Optional[str] = None
    contact_no: Optional[str] = None
    address: Optional[str] = None

class Member(MemberBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

# Borrowing Schemas
class BorrowingBase(BaseModel):
    book_id: int
    member_id: int

class BorrowingCreate(BorrowingBase):
    pass

class BorrowingReturn(BaseModel):
    borrowing_id: int

class Borrowing(BorrowingBase):
    id: int
    borrowed_date: datetime
    due_date: datetime
    returned_date: Optional[datetime]
    is_active: bool
    fine: float
    book: Book
    member: Member
    
    class Config:
        from_attributes = True

class BorrowingSimple(BorrowingBase):
    id: int
    borrowed_date: datetime
    due_date: datetime
    returned_date: Optional[datetime]
    is_active: bool
    fine: float
    
    class Config:
        from_attributes = True
