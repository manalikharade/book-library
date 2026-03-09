from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base

class Book(Base):
    __tablename__ = "books"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    author = Column(String, index=True)
    available = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationship
    borrowings = relationship("Borrowing", back_populates="book")

class Member(Base):
    __tablename__ = "members"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    contact_no = Column(String)
    address = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationship
    borrowings = relationship("Borrowing", back_populates="member")

class Borrowing(Base):
    __tablename__ = "borrowings"
    
    id = Column(Integer, primary_key=True, index=True)
    book_id = Column(Integer, ForeignKey("books.id"))
    member_id = Column(Integer, ForeignKey("members.id"))
    borrowed_date = Column(DateTime, default=datetime.utcnow)
    due_date = Column(DateTime)  # When the book should be returned
    returned_date = Column(DateTime, nullable=True)
    is_active = Column(Boolean, default=True)  # True if still borrowed, False if returned
    fine = Column(Float, default=0.0)  # Fine amount calculated when returned
    
    # Relationships
    book = relationship("Book", back_populates="borrowings")
    member = relationship("Member", back_populates="borrowings")
