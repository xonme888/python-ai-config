"""
GPU Memory Monitor
메모리 모니터링을 위한 주요 클래스들을 포함하는 모듈
"""

import logging
from .core.dependency import DependencyManager

# 기본 로거 설정
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
if not logger.handlers:
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    ))
    logger.addHandler(handler)

# 의존성 관리자 초기화
dep_manager = DependencyManager()


class GPUMemoryMonitor:
    """
    CPU와 GPU의 메모리 사용량을 모니터링하는 클래스
    """

    def __init__(self, use_gpu: bool = True):
        """
        초기화
        Args:
            use_gpu: GPU 모니터링 사용 여부
        """
        self._use_gpu = use_gpu
        self._cpu_monitor = None
        self._gpu_monitor = None

        # CPU 모니터 초기화
        if dep_manager.check_dependency("psutil", "5.9.0"):
            from .monitors.cpu import CPUMonitor

            self._cpu_monitor = CPUMonitor()

        # GPU 모니터 초기화
        if use_gpu:
            # CuPy 패키지 충돌 확인
            dep_manager.check_conflicts(["cupy-cuda11x", "cupy-cuda12x"])

            # GPU 모니터 설정
            if dep_manager.check_dependency(
                "cupy-cuda11x"
            ) or dep_manager.check_dependency("cupy-cuda12x"):
                import cupy as cp
                from .monitors.gpu import GPUMonitor

                self._gpu_monitor = GPUMonitor(cp)

    @property
    def has_gpu(self) -> bool:
        """GPU 모니터링 가능 여부"""
        return self._gpu_monitor is not None

    @property
    def has_cpu(self) -> bool:
        """CPU 모니터링 가능 여부"""
        return self._cpu_monitor is not None

    def print_cpu_memory(self, label: str = "") -> None:
        """
        현재 CPU 메모리를 출력한다.
        Args:
            label: 출력시 표시할 레이블
        """
        if not self._cpu_monitor:
            logger.warning("CPU monitoring is not available")
            return

        self._cpu_monitor.print_memory(label)

    def print_gpu_memory(self, label: str = "") -> None:
        """
        현재 GPU 메모리를 출력한다.
        Args:
            label: 출력시 표시할 레이블
        """
        if not self._gpu_monitor:
            logger.warning("GPU monitoring is not available")
            return

        self._gpu_monitor.print_memory(label)

    def print_memory_usage(
        self, label: str = "", include_cpu: bool = True
    ) -> None:
        """
        CPU와 GPU의 메모리 사용량을 모두 출력한다.
        Args:
            label: 출력시 표시할 레이블
            include_cpu: CPU 메모리도 함께 출력할지 여부
        """
        if label:
            logger.info(label)

        if include_cpu:
            self.print_cpu_memory()

        if self._use_gpu:
            self.print_gpu_memory()
