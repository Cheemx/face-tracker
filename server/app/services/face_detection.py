import logging
from typing import Optional

import mediapipe as mp
import numpy as np
from PIL import Image

logger = logging.getLogger(__name__)

_mp_face_detection = mp.solutions.face_detection
_detector = _mp_face_detection.FaceDetection(
    model_selection=0,
    min_detection_confidence=0.5,
)

def detect_face(image: Image.Image) -> Optional[dict]:
    """
    Run MediaPipe face detection on a PIL Image and return pixel-space ROI 
    for the first detected face, or None if no face is found.

    Returns:
        dict with keys {x, y, width, height} in absolute pixels, or None.
    """
    width, height = image.size

    rgb_array = np.array(image)

    results = _detector.process(rgb_array)

    if not results.detections:
        logger.info("No face detected in frame")
        return None
    
    detection = results.detections[0]
    bbox = detection.location_data.relative_bounding_box

    x = max(0, int(bbox.xmin * width))
    y = max(0, int(bbox.ymin * height))
    w = min(int(bbox.width * width), width - x)
    h = min(int(bbox.height * height), height - y)

    logger.info("Face detected: x=%d y=%d w=%d h=%d", x, y, w, h)
    return {"x": x, "y": y, "width": w, "height": h}