"""Memory information data structures."""

from dataclasses import dataclass


@dataclass
class MemoryInfo:
    """Memory usage information."""

    used: float  # in MB
    total: float  # in MB

    @property
    def free(self) -> float:
        """Get free memory in MB."""
        return self.total - self.used

    @property
    def usage_percent(self) -> float:
        """Get memory usage percentage."""
        if self.total == 0:
            return 0.0
        return (self.used / self.total) * 100

    def __str__(self) -> str:
        return f"{self.used:.2f} MB / {self.total:.2f} MB"
