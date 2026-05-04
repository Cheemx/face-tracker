"""
Unit tests for app.services.face_detection.

MediaPipe is mocked so no real model loading occurs.
"""

from unittest.mock import MagicMock, patch

import numpy as np
import pytest
from PIL import Image

from app.services import face_detection

def _make_image(width: int = 640, height: int = 480) -> Image.Image:
    """Create a blank RGB PIL image for testing."""
    return Image.fromarray(np.zeros((height, width, 3), dtype=np.uint8))

class TestDetectFace:
    def test_returns_none_when_no_detections(self):
        """detect_face returns None when MediaPipe finds no faces."""
        mock_results = MagicMock()
        mock_results.detections = []

        with patch.object(face_detection._detector, "process", return_value=mock_results):
            result = face_detection.detect_face(_make_image())

        assert result is None

    def test_returns_pixel_roi_for_single_face(self):
        """detect_face converts relative bbox to absolute pixel coordinates."""
        # Build a fake MediaPipe detection
        mock_bbox = MagicMock()
        mock_bbox.xmin = 0.1
        mock_bbox.ymin = 0.2
        mock_bbox.width = 0.3
        mock_bbox.height = 0.4

        mock_detection = MagicMock()
        mock_detection.location_data.relative_bounding_box = mock_bbox

        mock_results = MagicMock()
        mock_results.detections = [mock_detection]

        image = _make_image(width=640, height=480)

        with patch.object(face_detection._detector, "process", return_value=mock_results):
            result = face_detection.detect_face(image)

        assert result is not None
        assert result["x"] == int(0.1 * 640)   # 64
        assert result["y"] == int(0.2 * 480)   # 96
        assert result["width"] == int(0.3 * 640)  # 192
        assert result["height"] == int(0.4 * 480)  # 192

    def test_uses_only_first_detection(self):
        """detect_face should ignore additional detections beyond the first."""
        def _make_detection(xmin, ymin, w, h):
            mock_bbox = MagicMock()
            mock_bbox.xmin = xmin
            mock_bbox.ymin = ymin
            mock_bbox.width = w
            mock_bbox.height = h
            det = MagicMock()
            det.location_data.relative_bounding_box = mock_bbox
            return det

        mock_results = MagicMock()
        mock_results.detections = [
            _make_detection(0.1, 0.1, 0.2, 0.2),
            _make_detection(0.5, 0.5, 0.2, 0.2),  # should be ignored
        ]

        image = _make_image(width=100, height=100)

        with patch.object(face_detection._detector, "process", return_value=mock_results):
            result = face_detection.detect_face(image)

        assert result["x"] == 10  # 0.1 * 100

    def test_clamps_coordinates_within_image_bounds(self):
        """Negative or oversized relative coordinates are clamped to valid range."""
        mock_bbox = MagicMock()
        mock_bbox.xmin = -0.1   # negative — should clamp to 0
        mock_bbox.ymin = 0.0
        mock_bbox.width = 2.0   # oversized — should clamp to image width
        mock_bbox.height = 0.5

        mock_detection = MagicMock()
        mock_detection.location_data.relative_bounding_box = mock_bbox

        mock_results = MagicMock()
        mock_results.detections = [mock_detection]

        image = _make_image(width=100, height=100)

        with patch.object(face_detection._detector, "process", return_value=mock_results):
            result = face_detection.detect_face(image)

        assert result["x"] == 0            # clamped from -10
        assert result["width"] == 100      # clamped from 200
