"""
Unit tests for app.services.roi_service.

The repository layer and face detection service are mocked so no DB or
MediaPipe is required to run these tests.
"""

from unittest.mock import MagicMock, patch

import numpy as np
import pytest
from PIL import Image

from app.services import roi_service

def _make_base64_image() -> str:
    """Return a tiny valid base64-encoded JPEG string."""
    import base64
    import io

    img = Image.fromarray(np.zeros((100, 100, 3), dtype=np.uint8))
    buf = io.BytesIO()
    img.save(buf, format="JPEG")
    encoded = base64.b64encode(buf.getvalue()).decode()
    return f"data:image/jpeg;base64,{encoded}"

class TestProcessFrame:
    def test_returns_frame_and_roi_when_face_detected(self):
        """process_frame returns annotated frame and roi dict when a face is found."""
        fake_roi = {"x": 10, "y": 20, "width": 50, "height": 60}

        mock_db = MagicMock()

        with(
            patch("app.services.roi_service.face_detection.detect_face", return_value=fake_roi),
            patch("app.services.roi_service.roi_repository.save_roi") as mock_save,
        ):
            result = roi_service.process_frame(mock_db, _make_base64_image())

        assert "frame" in result
        assert result["frame"].startswith("data:image/jpeg;base64,")
        assert result["roi"] == fake_roi
        mock_save.assert_called_once_with(mock_db, x=10, y=20, width=50, height=60)

    def test_returns_frame_and_null_roi_when_no_face(self):
        """process_frame returns original frame and roi=None when no face detected."""
        mock_db = MagicMock()

        with (
            patch("app.services.roi_service.face_detection.detect_face", return_value=None),
            patch("app.services.roi_service.roi_repository.save_roi") as mock_save,
        ):
            result = roi_service.process_frame(mock_db, _make_base64_image())
        
        assert "frame" in result
        assert result["roi"] is None
        mock_save.assert_not_called()

    def test_does_not_save_roi_when_no_face_detected(self):
        """Repository save must not be called if MediaPipe finds no face."""
        mock_db = MagicMock()

        with (
            patch("app.services.roi_service.face_detection.detect_face", return_value=None),
            patch("app.services.roi_service.roi_repository.save_roi") as mock_save,
        ):
            roi_service.process_frame(mock_db, _make_base64_image())

        mock_save.assert_not_called()

class TestGetHistory:
    def test_returns_Serialized_roi_records(self):
        """get_history converts ORM objects to plain dicts."""
        from datetime import datetime

        mock_roi = MagicMock()
        mock_roi.id = "abc-123"
        mock_roi.timestamp = datetime(2024, 1, 15, 10, 30, 0)
        mock_roi.x = 5
        mock_roi.y = 10
        mock_roi.width = 100
        mock_roi.height = 120

        mock_db = MagicMock()

        with patch(
            "app.services.roi_service.roi_repository.get_last_50",
            return_value=[mock_roi]
        ):
            result = roi_service.get_history(mock_db)

        assert len(result) == 1
        assert result[0]["id"] == "abc-123"
        assert result[0]["x"] == 5
        assert result[0]["timestamp"] == "2024-01-15T10:30:00"

    def test_returns_empty_list_when_no_records(self):
        """get_history returns an empty list when DB has no ROI records."""
        mock_db = MagicMock()

        with patch(
            "app.services.roi_service.roi_repository.get_last_50",
            return_value=[],
        ):
            result = roi_service.get_history(mock_db)

        assert result == []