"""CPU memory monitor implementation."""

import psutil
from .base import MemoryMonitor
from ..core.converter import MemoryConverter
from ..core.info import MemoryInfo


class CPUMonitor(MemoryMonitor):
    """CPU 메모리 모니터링 클래스"""

    def get_memory_info(self) -> MemoryInfo:
        """CPU 메모리 정보 수집"""
        vm = psutil.virtual_memory()
        used = MemoryConverter.to_mb(vm.total - vm.available)
        total = MemoryConverter.to_mb(vm.total)
        return MemoryInfo(used, total)
