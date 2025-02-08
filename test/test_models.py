from unittest.mock import MagicMock

import pytest

from src.mini_scan.models import ScanData, Scans


@pytest.fixture
def mock_session():
    return MagicMock()

def test_insert_scan_data(mock_session):
    # Create a ScanData instance
    scan_data = ScanData(response_bytes_utf8=b"aGVsbG8gd29ybGQ=")

    # Add to session
    mock_session.add(scan_data)

    # Assert add was called
    mock_session.add.assert_called_with(scan_data)

def test_insert_scans(mock_session):
    # Create a Scans instance
    scan = Scans(
        ip="192.168.1.1",
        port=80,
        service="HTTP",
        timestamp=1672531199,
        data_version=1,
        data_id=1,
    )

    # Add to session
    mock_session.add(scan)

    # Assert add was called
    mock_session.add.assert_called_with(scan)
