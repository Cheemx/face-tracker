import logging
from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.services import roi_service

router = APIRouter()
logger = logging.getLogger(__name__)

@router.get("/roi", response_model=List[dict])
def get_roi_history(db: Session = Depends(get_db)):
    """Return the last 50 ROI records ordered by timestamp descending."""
    logger.info("GET /roi requested")
    return roi_service.get_history(db)