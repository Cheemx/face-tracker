import logging
from typing import List, Optional

from PIL import Image, ImageDraw
from sqlalchemy.orm import Session

from app.repository import roi_repository
from app.services import face_detection
from app.utils.image import decode_base64_image, encode_image_base64

logger = logging.getLogger(__name__)

_BOX_COLOR = (0, 255, 0) # bright green
_BOX_WIDTH = 3           # pixels

def process_frame(db: Session, base64_image: str) -> dict:
    """
    Full pipeline for a single webcam frame:

    1. Decode base64 → PIL Image
    2. Detect face with MediaPipe
    3. If face found: draw bounding box with Pillow & persist ROI to DB
    4. Re-encode annotated image to base64
    5. Return {frame, roi}

    Args:
        db:           SQLAlchemy session (injected by FastAPI).
        base64_image: Raw base64 string from the frontend WebSocket message.

    Returns:
        dict with keys:
            "frame" – base64-encoded annotated JPEG
            "roi"   – {x, y, width, height} dict or None
    """
    logger.info("Processing frame")

    image: Image.Image = decode_base64_image(base64_image)

    roi_data: Optional[dict] = face_detection.detect_face(image)

    if roi_data is not None:
        draw = ImageDraw.Draw(image)
        x, y, w, h = roi_data["x"], roi_data["y"], roi_data["width"], roi_data["height"]
        draw.rectangle(
            [x, y, x + w, y + h],
            outline=_BOX_COLOR,
            width=_BOX_WIDTH,
        )

        roi_repository.save_roi(db, x=x, y=y, width=w, height=h)
    
    encoded_frame = encode_image_base64(image)

    return {
        "frame": encoded_frame,
        "roi": roi_data,
    }

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