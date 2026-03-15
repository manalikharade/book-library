import logging

from fastapi import APIRouter, Depends, HTTPException

from .. import schemas
from ..dependencies import get_member_service
from ..services import MemberService

logger = logging.getLogger(__name__)
router = APIRouter(tags=["members"])

# Route order: list (GET /) before get (GET /{member_id}) so /api/members/ is unambiguous


@router.get("/", response_model=schemas.PaginatedResponse[schemas.Member])
def list_members(
    skip: int = 0,
    limit: int = 100,
    service: MemberService = Depends(get_member_service),
):
    """List all members with pagination (returns items and total count)."""
    items, total = service.list_paginated(skip=skip, limit=limit)
    return schemas.PaginatedResponse(items=items, total=total)


@router.post("/", response_model=schemas.Member)
def create_member(
    member: schemas.MemberCreate,
    service: MemberService = Depends(get_member_service),
):
    """Create a new member"""
    return service.create(member)


@router.get("/{member_id}", response_model=schemas.Member)
def read_member(
    member_id: int,
    service: MemberService = Depends(get_member_service),
):
    """Get a specific member by ID"""
    db_member = service.get(member_id)
    if db_member is None:
        raise HTTPException(status_code=404, detail="Member not found")
    return db_member


@router.put("/{member_id}", response_model=schemas.Member)
def update_member(
    member_id: int,
    member_update: schemas.MemberUpdate,
    service: MemberService = Depends(get_member_service),
):
    """Update a member's details"""
    db_member = service.update(member_id, member_update)
    if db_member is None:
        raise HTTPException(status_code=404, detail="Member not found")
    return db_member


@router.delete("/{member_id}")
def delete_member(
    member_id: int,
    service: MemberService = Depends(get_member_service),
):
    """Delete a member"""
    deleted = service.delete(member_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Member not found")
    return {"message": "Member deleted successfully"}
