import json
import logging

from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.services import roi_service

router = APIRouter()
logger = logging.getLogger(__name__)

@router.websocket("/ws/video")
async def video_websocket(websocket: WebSocket, db: Session = Depends(get_db)):
    """
    WebSocket endpoint for real-time face detection.

    Expects JSON messages: { "frame": "<base64 image string>" }
    Responds with JSON:    { "frame": "<base64 annotated image>", "roi": { x, y, width, height} | null }
    """
    await websocket.accept()
    logger.info("WebSocket client connected")

    try:
        while True:
            raw = await websocket.receive_text()

            try:
                payload = json.loads(raw)
                base64_image: str = payload["frame"]
            except (json.JSONDecodeError, KeyError) as exc:
                logger.error("Invalid WebSocket message: %s", exc)
                await websocket.send_text(json.dumps({"error": "Invalid message format"}))
                continue

            logger.info("Frame received via WebSocket")

            try:
                result = roi_service.process_frame(db, base64_image)
            except Exception as exc:
                logger.error("Error processing frame: %s", exc, exc_info=True)
                await websocket.send_text(json.dumps({"error": "Frame processing failed"}))
                continue

            await websocket.send_text(json.dumps(result))

    except WebSocketDisconnect:
        logger.info("WebSocket client disconnected")