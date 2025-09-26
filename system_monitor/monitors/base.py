"""Base monitor implementation."""

from abc import ABC, abstractmethod
from typing import Optional
from ..core import MemoryInfo
from ..logging_config import get_logger

logger = get_logger('system_monitor.monitors.base')


class BaseMonitor(ABC):
    """Base class for memory monitors."""

    def __init__(self):
        self._available = None

    @abstractmethod
    def get_memory_info(self) -> Optional[MemoryInfo]:
        """Get current memory information."""
        pass

    @property
    def is_available(self) -> bool:
        """Check if monitoring is available."""
        if self._available is None:
            try:
                info = self.get_memory_info()
                self._available = info is not None
            except Exception:
                self._available = False
        return self._available
