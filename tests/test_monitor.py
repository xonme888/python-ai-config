"""Main monitor tests."""

import pytest
from unittest.mock import Mock, patch
from system_monitor.monitor import (
    SystemMonitor,
    GPUMemoryMonitor,
    MemoryMonitorManager,
)
from system_monitor.core import MemoryInfo


class TestSystemMonitor:
    """Test main SystemMonitor class."""

    def test_init_default(self):
        """Test default initialization."""
        monitor = SystemMonitor()
        assert monitor._cpu_monitor is not None
        assert monitor._gpu_monitor is not None

    def test_init_no_gpu(self):
        """Test initialization without GPU."""
        monitor = GPUMemoryMonitor(use_gpu=False)
        assert monitor._cpu_monitor is not None
        assert monitor._gpu_monitor is None

    def test_init_with_cupy_instance(self):
        """Test initialization with custom CuPy instance."""
        mock_cupy = Mock()
        monitor = GPUMemoryMonitor(cupy_instance=mock_cupy)
        assert monitor._cpu_monitor is not None
        assert monitor._gpu_monitor is not None
        assert monitor._gpu_monitor._cupy is mock_cupy

    def test_has_cpu_property(self):
        """Test has_cpu property."""
        monitor = GPUMemoryMonitor(use_gpu=False)
        # Mock the CPU monitor to return available
        monitor._cpu_monitor._available = True
        assert monitor.has_cpu is True

        # Mock the CPU monitor to return unavailable
        monitor._cpu_monitor._available = False
        assert monitor.has_cpu is False

    def test_has_gpu_property_with_gpu(self):
        """Test has_gpu property when GPU monitor exists."""
        monitor = SystemMonitor()
        # Mock the GPU monitor to return available
        monitor._gpu_monitor._available = True
        assert monitor.has_gpu is True

        # Mock the GPU monitor to return unavailable
        monitor._gpu_monitor._available = False
        assert monitor.has_gpu is False

    def test_has_gpu_property_no_gpu(self):
        """Test has_gpu property when no GPU monitor."""
        monitor = GPUMemoryMonitor(use_gpu=False)
        assert monitor.has_gpu is False

    def test_get_cpu_memory(self):
        """Test get_cpu_memory method."""
        monitor = GPUMemoryMonitor(use_gpu=False)
        expected_info = MemoryInfo(used=100.0, total=200.0)

        # Mock the CPU monitor method
        monitor._cpu_monitor.get_memory_info = Mock(return_value=expected_info)

        info = monitor.get_cpu_memory()
        assert info is expected_info
        monitor._cpu_monitor.get_memory_info.assert_called_once()

    def test_get_gpu_memory_with_gpu(self):
        """Test get_gpu_memory method with GPU."""
        monitor = SystemMonitor()
        expected_info = MemoryInfo(used=50.0, total=100.0)

        # Mock the GPU monitor method
        monitor._gpu_monitor.get_memory_info = Mock(return_value=expected_info)

        info = monitor.get_gpu_memory()
        assert info is expected_info
        monitor._gpu_monitor.get_memory_info.assert_called_once()

    def test_get_gpu_memory_no_gpu(self):
        """Test get_gpu_memory method without GPU."""
        monitor = GPUMemoryMonitor(use_gpu=False)
        info = monitor.get_gpu_memory()
        assert info is None

    @patch("system_monitor.monitor.logger")
    def test_print_cpu_memory_success(self, mock_logger):
        """Test print_cpu_memory with successful info retrieval."""
        monitor = GPUMemoryMonitor(use_gpu=False)
        test_info = MemoryInfo(used=100.0, total=200.0)
        monitor._cpu_monitor.get_memory_info = Mock(return_value=test_info)

        monitor.print_cpu_memory("Test Label")

        mock_logger.info.assert_any_call("Test Label")
        mock_logger.info.assert_any_call(
            "  CPU: 100.00 MB / 200.00 MB (사용률: 50.0%)"
        )

    @patch("system_monitor.monitor.logger")
    def test_print_cpu_memory_failure(self, mock_logger):
        """Test print_cpu_memory with failed info retrieval."""
        monitor = GPUMemoryMonitor(use_gpu=False)
        monitor._cpu_monitor.get_memory_info = Mock(return_value=None)

        monitor.print_cpu_memory("Test Label")

        mock_logger.warning.assert_called_once_with(
            "Test Label: CPU memory info not available"
        )

    @patch("system_monitor.monitor.logger")
    def test_print_gpu_memory_success(self, mock_logger):
        """Test print_gpu_memory with successful info retrieval."""
        monitor = SystemMonitor()
        test_info = MemoryInfo(used=50.0, total=100.0)
        monitor._gpu_monitor.get_memory_info = Mock(return_value=test_info)

        monitor.print_gpu_memory("Test GPU")

        mock_logger.info.assert_any_call("Test GPU")
        mock_logger.info.assert_any_call(
            "  GPU: 50.00 MB / 100.00 MB (사용률: 50.0%)"
        )

    @patch("system_monitor.monitor.logger")
    def test_print_gpu_memory_failure(self, mock_logger):
        """Test print_gpu_memory with failed info retrieval."""
        monitor = SystemMonitor()
        monitor._gpu_monitor.get_memory_info = Mock(return_value=None)

        monitor.print_gpu_memory("Test GPU")

        mock_logger.warning.assert_called_once_with(
            "Test GPU: GPU memory info not available"
        )

    @patch("system_monitor.monitor.logger")
    def test_print_memory_usage_with_cpu(self, mock_logger):
        """Test print_memory_usage with CPU included."""
        monitor = SystemMonitor()
        cpu_info = MemoryInfo(used=100.0, total=200.0)
        gpu_info = MemoryInfo(used=50.0, total=100.0)

        monitor._cpu_monitor.get_memory_info = Mock(return_value=cpu_info)
        monitor._gpu_monitor.get_memory_info = Mock(return_value=gpu_info)

        monitor.print_memory_usage("System Status", include_cpu=True)

        mock_logger.info.assert_any_call("System Status")
        mock_logger.info.assert_any_call("  CPU: 100.00 MB / 200.00 MB")
        mock_logger.info.assert_any_call("  GPU: 50.00 MB / 100.00 MB")

    @patch("system_monitor.monitor.logger")
    def test_print_memory_usage_without_cpu(self, mock_logger):
        """Test print_memory_usage without CPU."""
        monitor = SystemMonitor()
        gpu_info = MemoryInfo(used=50.0, total=100.0)

        monitor._gpu_monitor.get_memory_info = Mock(return_value=gpu_info)

        monitor.print_memory_usage("GPU Only")

        mock_logger.info.assert_any_call("GPU Only")
        mock_logger.info.assert_any_call("  GPU: 50.00 MB / 100.00 MB")

    @patch("system_monitor.monitor.logger")
    def test_print_memory_usage_unavailable(self, mock_logger):
        """Test print_memory_usage with unavailable services."""
        monitor = SystemMonitor()

        monitor._cpu_monitor.get_memory_info = Mock(return_value=None)
        monitor._gpu_monitor.get_memory_info = Mock(return_value=None)

        monitor.print_memory_usage("Test", include_cpu=True)

        mock_logger.info.assert_any_call("Test")
        mock_logger.info.assert_any_call("  CPU: Not available")
        mock_logger.info.assert_any_call("  GPU: Not available")

    def test_memory_monitor_manager_alias(self):
        """Test that MemoryMonitorManager is an alias for GPUMemoryMonitor."""
        assert MemoryMonitorManager is GPUMemoryMonitor
