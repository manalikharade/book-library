"""Unit tests for Pydantic schema validation."""
import pytest
from pydantic import ValidationError

from app.schemas import BookCreate, BookUpdate, BorrowingCreate, BorrowingReturn, MemberCreate, MemberUpdate


def test_book_create_valid():
    b = BookCreate(title="Clean Code", author="Robert Martin")
    assert b.title == "Clean Code"
    assert b.author == "Robert Martin"


def test_book_create_title_empty_invalid():
    with pytest.raises(ValidationError):
        BookCreate(title="", author="Author")


def test_book_create_author_empty_invalid():
    with pytest.raises(ValidationError):
        BookCreate(title="Title", author="")


def test_member_create_valid():
    m = MemberCreate(name="Jane", contact_no="+123", address="Street 1")
    assert m.name == "Jane"


def test_member_create_name_empty_invalid():
    with pytest.raises(ValidationError):
        MemberCreate(name="", contact_no="+1", address="Addr")


def test_borrowing_create_ids_positive():
    b = BorrowingCreate(book_id=1, member_id=1)
    assert b.book_id == 1 and b.member_id == 1


def test_borrowing_create_book_id_zero_invalid():
    with pytest.raises(ValidationError):
        BorrowingCreate(book_id=0, member_id=1)


def test_borrowing_return_id_positive():
    r = BorrowingReturn(borrowing_id=1)
    assert r.borrowing_id == 1


def test_borrowing_return_id_zero_invalid():
    with pytest.raises(ValidationError):
        BorrowingReturn(borrowing_id=0)


def test_book_update_partial():
    u = BookUpdate(title="New Title")
    assert u.title == "New Title"
    assert u.author is None
