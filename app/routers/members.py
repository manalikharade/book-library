from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import schemas, crud
from ..database import get_db

router = APIRouter(tags=["members"])

@router.post("/", response_model=schemas.Member)
def create_member(member: schemas.MemberCreate, db: Session = Depends(get_db)):
    """Create a new member"""
    return crud.create_member(db=db, member=member)

@router.get("/{member_id}", response_model=schemas.Member)
def read_member(member_id: int, db: Session = Depends(get_db)):
    """Get a specific member by ID"""
    db_member = crud.get_member(db=db, member_id=member_id)
    if db_member is None:
        raise HTTPException(status_code=404, detail="Member not found")
    return db_member

@router.get("/", response_model=list[schemas.Member])
def list_members(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """List all members with pagination"""
    members = crud.get_all_members(db=db, skip=skip, limit=limit)
    return members

@router.put("/{member_id}", response_model=schemas.Member)
def update_member(member_id: int, member_update: schemas.MemberUpdate, db: Session = Depends(get_db)):
    """Update a member's details"""
    db_member = crud.update_member(db=db, member_id=member_id, member_update=member_update)
    if db_member is None:
        raise HTTPException(status_code=404, detail="Member not found")
    return db_member

@router.delete("/{member_id}")
def delete_member(member_id: int, db: Session = Depends(get_db)):
    """Delete a member"""
    db_member = crud.delete_member(db=db, member_id=member_id)
    if db_member is None:
        raise HTTPException(status_code=404, detail="Member not found")
    return {"message": "Member deleted successfully"}
