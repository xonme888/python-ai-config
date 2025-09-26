"""Core components tests."""

import pytest
from system_monitor.core.info import MemoryInfo
from system_monitor.core.converter import MemoryConverter


class TestMemoryInfo:
    """Test MemoryInfo data class."""

    def test_basic_properties(self):
        """Test basic properties of MemoryInfo."""
        info = MemoryInfo(used=1024.0, total=2048.0)
        assert info.used == 1024.0
        assert info.total == 2048.0
        assert info.free == 1024.0
        assert info.usage_percent == 50.0

    def test_zero_total(self):
        """Test behavior with zero total memory."""
        info = MemoryInfo(used=0.0, total=0.0)
        assert info.usage_percent == 0.0
        assert info.free == 0.0

    def test_str_representation(self):
        """Test string representation."""
        info = MemoryInfo(used=1024.0, total=2048.0)
        assert str(info) == "1024.00 MB / 2048.00 MB"

    def test_edge_cases(self):
        """Test edge cases."""
        # Used equals total
        info = MemoryInfo(used=1024.0, total=1024.0)
        assert info.usage_percent == 100.0
        assert info.free == 0.0


class TestMemoryConverter:
    """Test MemoryConverter utility."""

    def test_to_mb(self):
        """Test bytes to MB conversion."""
        bytes_value = 1024 * 1024  # 1MB in bytes
        mb_value = MemoryConverter.to_mb(bytes_value)
        assert mb_value == 1.0

    def test_to_gb(self):
        """Test bytes to GB conversion."""
        bytes_value = 1024 * 1024 * 1024  # 1GB in bytes
        gb_value = MemoryConverter.to_gb(bytes_value)
        assert gb_value == 1.0

    def test_format_memory_mb(self):
        """Test memory formatting in MB."""
        bytes_value = 1536 * 1024 * 1024  # 1.5GB
        formatted = MemoryConverter.format_memory(bytes_value, "MB")
        assert formatted == "1536.00 MB"

    def test_format_memory_gb(self):
        """Test memory formatting in GB."""
        bytes_value = 1536 * 1024 * 1024  # 1.5GB
        formatted = MemoryConverter.format_memory(bytes_value, "GB")
        assert formatted == "1.50 GB"

    def test_format_memory_default(self):
        """Test default memory formatting."""
        bytes_value = 1024 * 1024  # 1MB
        formatted = MemoryConverter.format_memory(bytes_value)
        assert formatted == "1.00 MB"

    def test_zero_bytes(self):
        """Test with zero bytes."""
        assert MemoryConverter.to_mb(0) == 0.0
        assert MemoryConverter.to_gb(0) == 0.0
        assert MemoryConverter.format_memory(0) == "0.00 MB"
