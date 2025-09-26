"""Logging configuration for system monitor."""

import logging
import sys
from typing import Optional

# 전역 로거 설정 상태 추적
_logger_configured = False


def setup_logger(
    name: Optional[str] = None,
    level: int = logging.INFO,
    force_setup: bool = False,
) -> logging.Logger:
    """
    시스템 모니터용 로거 설정.

    Colab과 VSCode 모두에서 동작하도록 최적화됨.

    Args:
        name: 로거 이름 (기본값: 'system_monitor')
        level: 로깅 레벨
        force_setup: 강제로 다시 설정할지 여부

    Returns:
        설정된 로거 인스턴스
    """
    global _logger_configured

    logger_name = name or "system_monitor"
    logger = logging.getLogger(logger_name)

    # 이미 설정되어 있고 강제 설정이 아니라면 기존 로거 반환
    if _logger_configured and not force_setup:
        return logger

    # 기존 핸들러 제거 (중복 방지)
    if logger.handlers:
        logger.handlers.clear()

    # 로거 레벨 설정
    logger.setLevel(level)

    # 콘솔 핸들러 생성
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)

    # Colab과 VSCode 모두에서 잘 보이는 포맷 설정
    formatter = logging.Formatter(
        "%(asctime)s - [%(name)s] - %(levelname)s - %(message)s",
        datefmt="%H:%M:%S",
    )
    console_handler.setFormatter(formatter)

    # 핸들러 추가
    logger.addHandler(console_handler)

    # 상위 로거로의 전파 방지 (중복 출력 방지)
    logger.propagate = False

    _logger_configured = True
    return logger


def get_logger(name: Optional[str] = None) -> logging.Logger:
    """
    시스템 모니터용 로거 가져오기.

    Args:
        name: 로거 이름 (기본값: 'system_monitor')

    Returns:
        로거 인스턴스
    """
    logger_name = name or "system_monitor"
    logger = logging.getLogger(logger_name)

    # 로거가 설정되지 않았다면 자동으로 설정
    if not logger.handlers:
        return setup_logger(logger_name)

    return logger


def reset_logger_config():
    """로거 설정 초기화."""
    global _logger_configured
    _logger_configured = False

    # 시스템 모니터 관련 모든 로거 리셋
    logger_names = [
        "system_monitor",
        "system_monitor.monitor",
        "system_monitor.monitors",
    ]
    for logger_name in logger_names:
        logger = logging.getLogger(logger_name)
        logger.handlers.clear()
        logger.setLevel(logging.NOTSET)
        logger.propagate = True


def is_colab() -> bool:
    """Google Colab 환경인지 확인."""
    try:
        import google.colab  # noqa: F401

        return True
    except ImportError:
        return False


def is_jupyter() -> bool:
    """Jupyter 환경인지 확인."""
    try:
        from IPython import get_ipython  # noqa: F401

        ipython = get_ipython()
        return ipython is not None and hasattr(ipython, "kernel")
    except ImportError:
        return False
