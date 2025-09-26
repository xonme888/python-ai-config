"""GPU memory monitor implementation."""

from typing import Any
from .base import MemoryMonitor
from ..core.converter import MemoryConverter
from ..core.info import MemoryInfo


class GPUMonitor(MemoryMonitor):
    """GPU 메모리 모니터링 클래스"""

    def __init__(self, cupy_instance: Any):
        self._cp = cupy_instance

    def get_memory_info(self) -> MemoryInfo:
        """GPU 메모리 정보 수집"""
        free, total = self._cp.cuda.runtime.memGetInfo()
        used = MemoryConverter.to_mb(total - free)
        total = MemoryConverter.to_mb(total)
        return MemoryInfo(used, total)
