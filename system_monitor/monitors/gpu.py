"""GPU memory monitoring."""

from typing import Optional
from .base import BaseMonitor
from ..core import MemoryInfo, MemoryConverter
from ..logging_config import get_logger

logger = get_logger('system_monitor.monitors.gpu')


class GPUMonitor(BaseMonitor):
    """GPU memory monitor using CuPy."""

    def __init__(self, cupy_instance=None):
        super().__init__()
        self._cupy = cupy_instance
        self._init_cupy()

    def _init_cupy(self):
        """Initialize CuPy."""
        if self._cupy is None:
            try:
                import cupy as cp

                self._cupy = cp
            except ImportError:
                logger.info("CuPy not available for GPU monitoring")
                self._cupy = None

    def get_memory_info(self) -> Optional[MemoryInfo]:
        """Get GPU memory information."""
        if not self._cupy:
            return None

        try:
            mempool = self._cupy.get_default_memory_pool()
            used_bytes = mempool.used_bytes()
            total_bytes = mempool.total_bytes()

            # If total is 0, try to get device memory info
            if total_bytes == 0:
                device = self._cupy.cuda.Device()
                total_bytes = device.mem_info[1]  # total memory
                used_bytes = total_bytes - device.mem_info[0]  # total - free

            used_mb = MemoryConverter.to_mb(used_bytes)
            total_mb = MemoryConverter.to_mb(total_bytes)

            return MemoryInfo(used=used_mb, total=total_mb)
        except Exception as e:
            logger.error(f"Failed to get GPU memory info: {e}")
            return None
