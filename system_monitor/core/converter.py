"""Memory unit conversion utilities."""


class MemoryConverter:
    """Memory unit conversion utilities."""

    @staticmethod
    def to_mb(bytes_value: float) -> float:
        """Convert bytes to megabytes."""
        return bytes_value / (1024 * 1024)

    @staticmethod
    def to_gb(bytes_value: float) -> float:
        """Convert bytes to gigabytes."""
        return bytes_value / (1024 * 1024 * 1024)

    @staticmethod
    def format_memory(bytes_value: float, unit: str = "MB") -> str:
        """Format memory value with unit."""
        if unit.upper() == "GB":
            value = MemoryConverter.to_gb(bytes_value)
            return f"{value:.2f} GB"
        else:
            value = MemoryConverter.to_mb(bytes_value)
            return f"{value:.2f} MB"
