"""System Monitor implementation."""

from typing import Optional
from .monitors import CPUMonitor, GPUMonitor
from .core import MemoryInfo
from .logging_config import get_logger

logger = get_logger('system_monitor.monitor')


class SystemMonitor:
    """Main system resource monitor for CPU and GPU memory."""

    def __init__(self, use_gpu: bool = True, cupy_instance=None):
        """
        Initialize memory monitor.

        Args:
            use_gpu: Whether to enable GPU monitoring
            cupy_instance: Custom CuPy instance to use
        """
        self._cpu_monitor = CPUMonitor()
        self._gpu_monitor = GPUMonitor(cupy_instance) if use_gpu else None

    @property
    def has_cpu(self) -> bool:
        """Check if CPU monitoring is available."""
        return self._cpu_monitor.is_available

    @property
    def has_gpu(self) -> bool:
        """Check if GPU monitoring is available."""
        return self._gpu_monitor is not None and self._gpu_monitor.is_available

    def get_cpu_memory(self) -> Optional[MemoryInfo]:
        """Get CPU memory information."""
        return self._cpu_monitor.get_memory_info()

    def get_gpu_memory(self) -> Optional[MemoryInfo]:
        """Get GPU memory information."""
        if not self._gpu_monitor:
            return None
        return self._gpu_monitor.get_memory_info()

    def print_cpu_memory(self, label: str = "CPU Memory") -> None:
        """Print CPU memory usage."""
        info = self.get_cpu_memory()
        if info:
            logger.info(f"{label}")
            logger.info(f"  CPU: {info} (사용률: {info.usage_percent:.1f}%)")
        else:
            logger.warning(f"{label}: CPU memory info not available")

    def print_gpu_memory(self, label: str = "GPU Memory") -> None:
        """Print GPU memory usage."""
        info = self.get_gpu_memory()
        if info:
            logger.info(f"{label}")
            logger.info(f"  GPU: {info} (사용률: {info.usage_percent:.1f}%)")
        else:
            logger.warning(f"{label}: GPU memory info not available")

    def print_memory_usage(
        self, label: str = "Memory Status", include_cpu: bool = False
    ) -> None:
        """Print overall memory usage."""
        logger.info(f"{label}")

        if include_cpu:
            cpu_info = self.get_cpu_memory()
            if cpu_info:
                logger.info(f"  CPU: {cpu_info}")
            else:
                logger.info("  CPU: Not available")

        gpu_info = self.get_gpu_memory()
        if gpu_info:
            logger.info(f"  GPU: {gpu_info}")
        else:
            logger.info("  GPU: Not available")


# 하위 호환성을 위한 별칭
GPUMemoryMonitor = SystemMonitor
MemoryMonitorManager = SystemMonitor
