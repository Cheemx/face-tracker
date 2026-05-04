import logging
from typing import List, Optional

from sqlalchemy.orm import Session

from app.models.roi import ROI

logger = logging.getLogger(__name__)

def get_last_50(db: Session) -> List[ROI]:
    """Return the last 50 ROI records ordered by timestamp descending."""
    return (
        db.query(ROI)
        .order_by(ROI.timestamp.desc())
        .limit(50)
        .all()
    )