import logging
from typing import List, Optional

from sqlalchemy.orm import Session

from app.models.roi import ROI

logger = logging.getLogger(__name__)

def save_roi(db: Session, x: int, y: int, width: int, height: int) -> ROI:
    """Insert a new ROI record into the database."""
    roi = ROI(x=x, y=y, width=width, height=height)
    db.add(roi)
    db.commit()
    db.refresh(roi)
    logger.info("Saved ROI id=%s x=%d y=%d w=%d h=%d", roi.id, x, y, width, height)
    return roi

def get_last_50(db: Session) -> List[ROI]:
    """Return the last 50 ROI records ordered by timestamp descending."""
    return (
        db.query(ROI)
        .order_by(ROI.timestamp.desc())
        .limit(50)
        .all()
    )