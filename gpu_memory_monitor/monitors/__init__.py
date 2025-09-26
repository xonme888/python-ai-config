"""Monitors package initialization."""

from .cpu import CPUMonitor
from .gpu import GPUMonitor

__all__ = ["CPUMonitor", "GPUMonitor"]
