"""Base memory monitor interface."""

import logging
from abc import ABC, abstractmethod
from ..core.info import MemoryInfo

logger = logging.getLogger(__name__)


class MemoryMonitor(ABC):
    """메모리 모니터링 기본 클래스"""

    @abstractmethod
    def get_memory_info(self) -> MemoryInfo:
        """메모리 정보 수집"""
        pass

    def format_output(
        self, label: str, memory_type: str, memory_info: MemoryInfo
    ) -> str:
        """메모리 정보 출력 형식을 생성"""
        return f"{label}\n  {memory_type}: {memory_info}"

    def print_memory(self, label: str = "") -> None:
        """메모리 정보를 출력"""
        memory_info = self.get_memory_info()
        memory_type = self.__class__.__name__.replace("Monitor", "")
        logger.info(self.format_output(label, memory_type, memory_info))
