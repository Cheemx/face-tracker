import base64
import io
import logging

from PIL import Image

logger = logging.getLogger(__name__)

def decode_base64_image(data: str) -> Image.Image:
    """Decode a base64 string (with or without data-URI prefix) into a PIL Image."""
    # Strip the data-URI prefix if present
    if "," in data:
        data = data.split(",", 1)[1]
    raw = base64.b64decode(data)
    image = Image.open(io.BytesIO(raw)).convert("RGB")
    return image

def encode_image_base64(image: Image.Image, fmt: str = "JPEG") -> str:
    """Enode a PIL Image to a base64 string."""
    buffer = io.BytesIO()
    image.save(buffer, format=fmt, quality=85)
    encoded = base64.b64encode(buffer.getvalue()).decode("utf-8")
    return f"data:image/jpeg;base64,{encoded}"