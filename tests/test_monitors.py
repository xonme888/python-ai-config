"""Monitor components tests - simplified version."""

import pytest
from unittest.mock import Mock, patch
from system_monitor.monitors.base import BaseMonitor
from system_monitor.monitors.cpu import CPUMonitor
from system_monitor.monitors.gpu import GPUMonitor
from system_monitor.core import MemoryInfo


class TestBaseMonitor:
    """Test BaseMonitor abstract class."""

    def test_abstract_methods(self):
        """Test that BaseMonitor cannot be instantiated."""
        with pytest.raises(TypeError):
            BaseMonitor()

    def test_is_available_caching(self):
        """Test availability caching."""

        class MockMonitor(BaseMonitor):
            def __init__(self):
                super().__init__()
                self.call_count = 0

            def get_memory_info(self):
                self.call_count += 1
                return MemoryInfo(used=100.0, total=200.0)

        monitor = MockMonitor()
        # First call should invoke get_memory_info
        assert monitor.is_available is True
        assert monitor.call_count == 1

        # Second call should use cached result
        assert monitor.is_available is True
        assert monitor.call_count == 1

    def test_is_available_exception_handling(self):
        """Test is_available exception handling."""

        class ErrorMonitor(BaseMonitor):
            def get_memory_info(self):
                raise RuntimeError("Test error")

        monitor = ErrorMonitor()
        # Should handle exception and return False
        assert monitor.is_available is False


class TestCPUMonitor:
    """Test CPUMonitor class."""

    def test_init_without_psutil(self):
        """Test initialization when psutil is not available."""
        with patch("builtins.__import__", side_effect=ImportError):
            monitor = CPUMonitor()
            assert monitor._psutil is None

    def test_get_memory_info_no_psutil(self):
        """Test memory info when psutil is not available."""
        monitor = CPUMonitor()
        monitor._psutil = None
        info = monitor.get_memory_info()
        assert info is None

    def test_get_memory_info_success(self):
        """Test successful memory info retrieval."""
        monitor = CPUMonitor()
        # Mock psutil after initialization
        mock_psutil = Mock()
        mock_psutil.virtual_memory.return_value = Mock(
            used=1024 * 1024 * 1024,  # 1GB in bytes
            total=2048 * 1024 * 1024,  # 2GB in bytes
        )
        monitor._psutil = mock_psutil

        info = monitor.get_memory_info()
        assert info is not None
        assert info.used == 1024.0  # 1GB in MB
        assert info.total == 2048.0  # 2GB in MB

    def test_get_memory_info_exception(self):
        """Test memory info when psutil raises exception."""
        monitor = CPUMonitor()
        mock_psutil = Mock()
        mock_psutil.virtual_memory.side_effect = Exception("Test error")
        monitor._psutil = mock_psutil

        info = monitor.get_memory_info()
        assert info is None

    def test_is_available_property(self):
        """Test is_available property."""
        monitor = CPUMonitor()
        # Test when psutil is None
        monitor._psutil = None
        assert monitor.is_available is False

        # Test when psutil is available
        mock_psutil = Mock()
        mock_psutil.virtual_memory.return_value = Mock(
            used=1024 * 1024 * 1024, total=2048 * 1024 * 1024
        )
        monitor._psutil = mock_psutil
        monitor._available = None  # Reset cache
        assert monitor.is_available is True


class TestGPUMonitor:
    """Test GPUMonitor class."""

    def test_init_without_cupy(self):
        """Test initialization when CuPy is not available."""
        with patch("builtins.__import__", side_effect=ImportError):
            monitor = GPUMonitor()
            assert monitor._cupy is None

    def test_init_with_cupy_instance(self):
        """Test initialization with custom CuPy instance."""
        mock_cupy = Mock()
        monitor = GPUMonitor(cupy_instance=mock_cupy)
        assert monitor._cupy is mock_cupy

    def test_get_memory_info_success(self):
        """Test successful GPU memory info retrieval."""
        mock_cupy = Mock()
        mempool = Mock()
        mempool.used_bytes.return_value = 512 * 1024 * 1024  # 512MB
        mempool.total_bytes.return_value = 1024 * 1024 * 1024  # 1GB
        mock_cupy.get_default_memory_pool.return_value = mempool

        monitor = GPUMonitor(cupy_instance=mock_cupy)
        info = monitor.get_memory_info()

        assert info is not None
        assert info.used == 512.0  # 512MB
        assert info.total == 1024.0  # 1GB

    def test_get_memory_info_zero_total(self):
        """Test memory info when mempool total is zero."""
        mock_cupy = Mock()
        # Setup mock for zero total bytes scenario
        mempool = Mock()
        mempool.used_bytes.return_value = 0
        mempool.total_bytes.return_value = 0
        mock_cupy.get_default_memory_pool.return_value = mempool

        device = Mock()
        device.mem_info = (
            512 * 1024 * 1024,
            1024 * 1024 * 1024,
        )  # (free, total)
        mock_cupy.cuda.Device.return_value = device

        monitor = GPUMonitor(cupy_instance=mock_cupy)
        info = monitor.get_memory_info()

        assert info is not None
        assert info.used == 512.0  # From device info
        assert info.total == 1024.0

    def test_get_memory_info_no_cupy(self):
        """Test memory info when CuPy is not available."""
        monitor = GPUMonitor()
        monitor._cupy = None
        info = monitor.get_memory_info()
        assert info is None

    def test_get_memory_info_exception(self):
        """Test memory info when CuPy raises exception."""
        mock_cupy = Mock()
        mock_cupy.get_default_memory_pool.side_effect = Exception("Test error")

        monitor = GPUMonitor(cupy_instance=mock_cupy)
        info = monitor.get_memory_info()

        assert info is None

    def test_is_available_property(self):
        """Test is_available property."""
        # Test when cupy is None
        monitor = GPUMonitor()
        monitor._cupy = None
        assert monitor.is_available is False

        # Test when cupy is available
        mock_cupy = Mock()
        mempool = Mock()
        mempool.used_bytes.return_value = 512 * 1024 * 1024
        mempool.total_bytes.return_value = 1024 * 1024 * 1024
        mock_cupy.get_default_memory_pool.return_value = mempool

        monitor = GPUMonitor(cupy_instance=mock_cupy)
        monitor._available = None  # Reset cache
        assert monitor.is_available is True
