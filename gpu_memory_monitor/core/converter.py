"""Memory unit conversion utilities."""


class MemoryConverter:
    """메모리 단위 변환을 담당하는 클래스"""

    BYTES_TO_MB = 1024 * 1024

    @classmethod
    def to_mb(cls, bytes_value: int) -> float:
        """바이트를 메가바이트로 변환"""
        return bytes_value / cls.BYTES_TO_MB
