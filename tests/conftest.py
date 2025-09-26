"""Test configuration and fixtures."""

import pytest
import logging
from unittest.mock import Mock


@pytest.fixture
def mock_psutil():
    """Mock psutil for testing."""
    mock = Mock()
    mock.virtual_memory.return_value = Mock(
        used=1024 * 1024 * 1024,  # 1GB in bytes
        total=2048 * 1024 * 1024,  # 2GB in bytes
    )
    return mock


@pytest.fixture
def mock_cupy():
    """Mock CuPy for testing."""
    mock = Mock()
    mempool = Mock()
    mempool.used_bytes.return_value = 512 * 1024 * 1024  # 512MB
    mempool.total_bytes.return_value = 1024 * 1024 * 1024  # 1GB
    mock.get_default_memory_pool.return_value = mempool

    device = Mock()
    device.mem_info = (512 * 1024 * 1024, 1024 * 1024 * 1024)  # (free, total)
    mock.cuda.Device.return_value = device

    return mock


@pytest.fixture(autouse=True)
def setup_logging():
    """Setup logging for tests."""
    logging.basicConfig(level=logging.INFO)
