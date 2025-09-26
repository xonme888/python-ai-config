"""System Monitor - A comprehensive system resource monitoring library."""

from .monitor import SystemMonitor, GPUMemoryMonitor, MemoryMonitorManager
from .core import MemoryInfo, MemoryConverter
from .logging_config import setup_logger, get_logger, reset_logger_config
from .env_utils import (
    detect_environment,
    print_environment_info,
    setup_environment_optimized_monitor
)

__version__ = "0.3.1"
__all__ = [
    'SystemMonitor',        # 새로운 메인 클래스
    'GPUMemoryMonitor',     # 하위 호환성
    'MemoryMonitorManager',  # 하위 호환성
    'MemoryInfo',
    'MemoryConverter',
    'setup_logger',         # 로깅 설정
    'get_logger',          # 로거 가져오기
    'reset_logger_config',  # 로거 리셋
    'detect_environment',   # 환경 감지
    'print_environment_info',  # 환경 정보 출력
    'setup_environment_optimized_monitor'  # 환경 최적화 모니터
]
