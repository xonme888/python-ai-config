"""Memory information data structures."""

from dataclasses import dataclass


@dataclass
class MemoryInfo:
    """메모리 정보를 저장하는 데이터 클래스"""

    used: float
    total: float

    def __str__(self) -> str:
        return f"{self.used:.2f} MB / {self.total:.2f} MB"
