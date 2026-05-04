"""
Unit tests for app.services.roi_service.

The repository layer and face detection service are mocked so no DB or
MediaPipe is required to run these tests.
"""

from unittest.mock import MagicMock, patch

import pytest

from app.services import roi_service

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