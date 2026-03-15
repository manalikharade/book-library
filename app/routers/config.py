from fastapi import APIRouter
from pydantic import BaseModel
from ..config import get_settings

router = APIRouter(prefix="/config", tags=["configuration"])

class BorrowingConfig(BaseModel):
    """Borrowing configuration"""
    borrowing_duration_days: int
    fine_per_day: float
    max_fine: float

@router.get("/borrowing", response_model=BorrowingConfig)
def get_borrowing_config():
    """Get borrowing configuration (duration and fine settings)"""
    settings = get_settings()
    return {
        "borrowing_duration_days": settings.borrowing_duration_days,
        "fine_per_day": settings.fine_per_day,
        "max_fine": settings.max_fine
    }

@router.get("/settings")
def get_all_settings():
    """Get all application settings (for admin purposes)"""
    settings = get_settings()
    return {
        "borrowing": {
            "duration_days": settings.borrowing_duration_days,
            "fine_per_day": settings.fine_per_day,
            "max_fine": settings.max_fine
        },
        "api": {
            "title": settings.api_title,
            "version": settings.api_version
        },
        "environment": settings.environment
    }
