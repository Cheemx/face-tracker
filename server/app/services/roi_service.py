import logging
from typing import List, Optional

from sqlalchemy.orm import Session

from app.repository import roi_repository

logger = logging.getLogger(__name__)

def get_history(db: Session) -> List[dict]:
    """Returns the last 50 ROI records as plain dicts."""
    records = roi_repository.get_last_50(db)
    return [
        {
            "id": r.id,
            "timestamp": r.timestamp.isoformat(),
            "x": r.x,
            "y": r.y,
            "width": r.width,
            "height": r.height,
        }
        for r in records
    ]