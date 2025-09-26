"""CPU memory monitoring."""

from typing import Optional
from .base import BaseMonitor
from ..core import MemoryInfo, MemoryConverter
from ..logging_config import get_logger

logger = get_logger('system_monitor.monitors.cpu')


class CPUMonitor(BaseMonitor):
    """CPU memory monitor using psutil."""

    def __init__(self):
        super().__init__()
        self._psutil = None
        self._init_psutil()

    def _init_psutil(self):
        """Initialize psutil."""
        try:
            import psutil

            self._psutil = psutil
        except ImportError:
            logger.warning("psutil not available for CPU monitoring")
            self._psutil = None

    def get_memory_info(self) -> Optional[MemoryInfo]:
        """Get CPU memory information."""
        if not self._psutil:
            return None

        try:
            memory = self._psutil.virtual_memory()
            used_mb = MemoryConverter.to_mb(memory.used)
            total_mb = MemoryConverter.to_mb(memory.total)
            return MemoryInfo(used=used_mb, total=total_mb)
        except Exception as e:
            logger.error(f"Failed to get CPU memory info: {e}")
            return None
